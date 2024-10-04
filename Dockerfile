# Dockerイメージを作成するための手順を記述したファイル

# FROM：Dockerイメージのベースとなるイメージを指定
# https://hub.docker.com/_/python
# Python を実行するための必要最小限のツールとパッケージが含まれているイメージを指定
FROM python:3.12-slim

# WORKDIR：コマンドを実行する作業ディレクトリを指定（ディレクトリ app を指定）
WORKDIR /app

# COPY：ローカルのファイルやディレクトリをDockerイメージ内にコピー
# COPY コピー元 コピー先
COPY . /app

# RUN：Dockerイメージ作成時（ビルド時）に実行するコマンドを指定
# 必要なライブラリをインストール
RUN pip install -r requirements.txt

# CMD：Dockerコンテナ起動時に実行するコマンド
# CMD ["python", "main.py"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app