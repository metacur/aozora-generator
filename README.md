\# Overview

文学作品の紹介文を生成AIを使って生成するスクリプトです。<br />

作家名と作品名は青空文庫から取得しています。<br /><br />



OpenAI API KEYの設定が必要です。<br />

※※環境変数などで安全に管理してください※※<br /><br />





# 生成する紹介文とは<br />

\- あらすじ

\- キャッチフレーズ

\- 著名人による帯コメント風の文章





\# Prerequisites

Python

OpenAI API Key



\# Requirements

Flask

openai

requests

beautifulsoup4

render\_template

jsonify

chardet



\# USAGE

python app.py

\- 作家名と作品名を選択

\- 紹介文を生成ボタンを押す

