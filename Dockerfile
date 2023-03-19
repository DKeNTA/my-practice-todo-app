# ベースイメージの指定
FROM python:3.9
# バッファにデータを保持しない設定(1でなくても任意の文字でいい)
ENV PYTHONUNBUFFERD 1
# コンテナの中にディレクトリを作成
RUN mkdir /app
# 作業ディレクトリの設定
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/