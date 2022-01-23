# boushi2

ラズパイに接続された光センサの値を読んで部屋の開閉状態を通知するBot。Slackの[Slash Commands](https://api.slack.com/interactivity/slash-commands)を利用して`/boushitsu`と入力すると通知が返ってくる。

依存ライブラリはこれ

- [Bolt for Python](https://github.com/slackapi/bolt-python)
- [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/code) (ラズパイには最初から入っている)

## 光センサ(cds)

## 前準備 Slack Botの作成

0. Slack Botを作成しておく。

### App Token(SocketModeでWebSocketの経路を開くために必要)

1. アプリの設定画面

![slackbot_setting_page](https://user-images.githubusercontent.com/61489178/150679024-24cfa277-4f84-48a0-b652-fa4e9978f60c.png)

をスクロールして出てくるApp-Level TokensのところのGenerate Token and Scopesをクリックする。

2. スコープ`connections:write`を持つトークンを生成する。

生成できると以下のようになる。

![app_token](https://user-images.githubusercontent.com/61489178/150678821-d5c3ba28-f803-4173-8bc8-ca82fac1afdf.png)

### Bot Token

1. アプリの設定画面に出ているこのトークンを使用する。

![bot_token](https://user-images.githubusercontent.com/61489178/150679234-77985303-3df6-4d69-8eb4-6106c178df06.png)

### manifestファイル

自動生成されるが一応参考までに。

```yaml
display_information:
  name: boushitsu
  description: boushitsu
features:
  bot_user:
    display_name: boushitsu
    always_online: false
  slash_commands:
    - command: /boushitsu
      description: boushitsu
      should_escape: false
oauth_config:
  scopes:
    bot:
      - commands
settings:
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
```

## インストールと起動

1. 依存ライブラリをインストール。

> 仮想環境(この文書では[この仮想環境](https://docs.python.org/ja/3/library/venv.html#venv-def)を指す)を無理に使う必要は無いが、もし使うならRPi.GPIOも改めてインストールしないと見えないのでインストール。このときRPi.GPIOのビルドが落ちるかもしれないが、以下のようにCFLAGSを設定することで回避できる(work around)。

```bash
# Python 3.6+ required
python -m venv .venv # 2系と3系が共存している環境ではpython3コマンドを使用せよ
source .venv/bin/activate

pip install -U pip
CFLAGS=-fcommon pip install -U -r requirements.txt
```

2. 環境変数にトークンを設定して起動する。

```bash
export SLACK_APP_TOKEN=<your-xapp-token>
export SLACK_BOT_TOKEN=<your-xoxb-token>
python main.py
```

## 永続化

実際運用するときはサービスとして動かすものと思う。[pm2](https://github.com/Unitech/pm2)向けの設定ファイルがある。Node.js向けだが、使えるのでいいでしょう。

1. pm2そのものを[公式](https://pm2.keymetrics.io/docs/usage/quick-start/)にしたがってセットアップしておく。

2. 設定ファイル例をコピーする。

```bash
cp ecosystem.config.js.example ecosystem.config.js
```

3. コピーしてできた本チャンの設定ファイルを好きなエディタで編集する。各トークン、`SLACK_APP_TOKEN`(`xapp-`で始まるトークン)と`SLACK_BOT_TOKEN`(`xoxb-`で始まるトークン)を設定する。

    なお、設定ファイルは仮想環境向けに書いてあるが、仮想環境を使わない場合は`interpreter`のところを`python3`に書き換えること。

4. 起動する。

```bash
pm2 start ecosystem.config.js
pm2 save # pm2のserviceが動いている前提
```
