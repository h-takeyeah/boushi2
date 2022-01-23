# boushi2

ラズパイに接続された光センサの値を読んで部屋の開閉状態を通知するBot。Slackの[Slash Commands](https://api.slack.com/interactivity/slash-commands)を利用して`/boushitsu`と入力すると通知が返ってくる。

## 光センサ(cds)

## インストールと起動

```bash
python -m venv .venv # 2系と3系が共存している環境ではpython3コマンドを使用せよ
source .venv/bin/activate
pip install -U -r requirements.txt
```

トークンを設定して起動する。

```bash
export SLACK_APP_TOKEN=<your-xapp-token>
export SLACK_APP_TOKEN=<your-xapp-token>
python main.py
```

## 永続化

実際運用するときはサービスとして動かすものと思う。[pm2](https://github.com/Unitech/pm2)向けの設定ファイルがある。Node.js向けだが、使えるのでいいでしょう。pm2そのものは[公式](https://pm2.keymetrics.io/docs/usage/quick-start/)にしたがってセットアップしておく。

あとはコピーして`SLACK_BOT_TOKEN`(`xoxb-`で始まるトークン)と`SLACK_APP_TOKEN`(`xapp-`で始まるトークン)を設定する。

```bash
cp ecosystem.config.js.example ecosystem.config.js
vim ecosystem.config.js # SLACK_APP_TOKENとSLACK_BOT_TOKENを適切に設定する
```

起動する。

```bash
pm2 start ecosystem.config.js
pm2 save # pm2のserviceが動いている前提
```

