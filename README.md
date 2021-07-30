# Description

FastAPI と MySQL を用いた API サーバーのプロジェクト

# Install

create docker

```
$ docker-compose up -d --build
```

## db schema

コンテナ初回作成時に docker/mysql/initdb.d 配下の.sql ファイルを実行する。

## db settings

環境変数で指定する。

```
DB_USER : DB ユーザー
DB_PASSWORD : DB パスワード
DB_HOST : DB ホスト名
DB_DATABASE_NAME : DB 名
```

# port 変更

下記を変更することで参照ポートを変更できる

## docker-compose.yml

```
services / api / ports
```

## docker/api/Dockerfile

```
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "9000"]
の
"--port", "9000"
を変更する
```
