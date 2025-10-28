# Overview
- 文学作品の紹介文を生成AIを使って生成するスクリプトです。
- 作家名と作品名は青空文庫から取得しています。<br />

- OpenAI API KEYの設定が必要です。<br />
- ※※環境変数などで安全に管理してください※※<br />

# 生成する紹介文とは
- あらすじ
- キャッチフレーズ
- 著名人による帯コメント風の文章

# Prerequisites
Python<br />
OpenAI API Key

# Requirements
Flask<br />
openai<br />
requests<br />
beautifulsoup4<br />
render_template<br />
jsonify<br />
chardet<br />

# USAGE
python app.py<br />
http://localhost:5000/ にアクセス
- 作家名と作品名を選択
- 紹介文を生成ボタンを押す



