# The telegram Bot

這是一個會定時提醒你事情的 Telegram Bot，提供圖形化介面快速、簡潔的設定提醒時間。若提醒事項為吃藥，還會串接網路 API 提供藥品資訊，避免不知道副作用的情況就將要稀裡糊塗吃下去了。

## Basic Usage

```
/new_reamind 創建新的提醒事項
/show_remind 查看現有提醒事項
/del_remind 刪除現有提醒事項
```

## Install

將整個儲存庫 clone 的本機中：

```sh
git clone https://github.com/simanglam/telebot.git
```

下載所需 module

```sh
pip install -r requirements.txt
```

建立一名為 token.json 的檔案，並在裡面打上以下內容：

```json
{
    "token": "你的 Bot Token"
}
```

請用你向 BotFather 申請的 Bot Token 替換掉 "你的 Bot Token" 這串。