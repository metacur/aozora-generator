from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import chardet
from flask_cors import CORS
from urllib.parse import urljoin, urlsplit, urlunsplit

app = Flask(__name__)
CORS(app)


# OpenAI APIキーを設定（環境変数などで安全に管理してください）
openai.api_key = "YOUR_API_KEY"



# 作家一覧を取得
def get_authors():
    url = "https://www.aozora.gr.jp/index_pages/person_all.html"
    res = requests.get(url)
    res.encoding = "shift_jis"
    detected = chardet.detect(res.content)
    encoding = detected['encoding'] if detected['confidence'] > 0.5 else 'shift_jis'
    text = res.content.decode(encoding, errors='replace')

    soup = BeautifulSoup(text, "html.parser")
    authors = {}
    for li in soup.select("ol > li"):
        a = li.find("a")
        if a and "href" in a.attrs:
            name = a.text.strip()
            link = urljoin(url, a["href"])
            authors[name] = link

    print(f"取得した作家数: {len(authors)}")  # ログ出力
    return authors


# 作品一覧を取得
def get_titles(author_url):
    # URLのアンカー（#以降）を除去
    author_url = author_url.split("#")[0]
    print(f"アクセスURL: {author_url}")  # ログ出力

    res = requests.get(author_url)
    detected = chardet.detect(res.content)
    encoding = detected['encoding'] if detected['confidence'] > 0.5 else 'shift_jis'
    text = res.content.decode(encoding, errors='replace')

    soup = BeautifulSoup(text, "html.parser")
    titles = []

    # <ol><li><a> の構造から作品名を抽出
    for li in soup.select("ol > li"):
        a = li.find("a")
        if a and "../cards/" in a.get("href", ""):
            title = a.text.strip()
            titles.append(title)

    print(f"取得作品数: {len(titles)}")  # ログ出力
    return titles






# 生成AIで紹介文を作成
def generate_ai_summary(author, title):
    prompt = f"""
以下は青空文庫に収録されている文学作品「{title}」についての紹介文を生成する指示です。

1. あらすじ（200文字程度）
2. キャッチフレーズ（短く印象的に）
3. 著名人が帯に書きそうなコメント（著名人名は架空でもOK）

作品タイトル: {title}
著者: {author}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは日本文学に詳しい編集者です。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']


# トップページ表示
@app.route("/")
def index():
    authors = get_authors()
    return render_template("index.html", authors=authors)

# 作品一覧取得（Ajax用）
@app.route("/get_titles", methods=["POST"])
def get_titles_route():
    data = request.get_json()
    raw_url = data.get("url")
    clean_url = raw_url.split("#")[0]
    titles = get_titles(clean_url)
    return jsonify(titles)

# 紹介文生成（Ajax用）
@app.route("/generate_ai", methods=["POST"])
def generate_ai_route():
    data = request.get_json()
    author = data.get("author")
    title = data.get("title")
    result = generate_ai_summary(author, title)
    return jsonify({"result": result})

# アプリ起動
if __name__ == "__main__":
    app.run(debug=True)