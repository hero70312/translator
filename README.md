# Telegram 印尼文／中文翻譯機器人

收到中文時翻譯成印尼文；收到印尼文時翻譯成繁體中文。

## 準備憑證

1. 在 Telegram 找 `@BotFather`，使用 `/newbot` 建立機器人並取得 bot token。
2. 到 DeepL API 申請 API key。e
3. 複製 `.env.example` 為 `.env`，填入兩組憑證。`.env` 不會加入 Git。

## 執行

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
set -a
source .env
set +a
python bot.py
```

啟動後，在 Telegram 開啟 bot 對話並傳送文字即可翻譯。也可以使用 `/start` 查看提示。
