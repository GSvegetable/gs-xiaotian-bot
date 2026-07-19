import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 从 Railway 的环境变量中读取 Token (更安全)
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ================= 轻量保活网页 =================
app = Flask(__name__)
@app.route('/')
def home():
    return "小恬在运行..."

def run_web():
    app.run(host="0.0.0.0", port=8080)

# ================= 机器人核心逻辑 =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好！我是小恬。有事说事，发1拉黑哦。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 只有遇到“在吗”才回复，其他文字一概无视
    if update.message.text == "在吗":
        await update.message.reply_text("有事说事看到了会回复别发1发1拉黑")

def main():
    # 1. 启动保活网页（放在后台线程）
    Thread(target=run_web, daemon=True).start()

    # 2. 启动机器人
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ 小恬机器人已上线！")
    application.run_polling()

if __name__ == "__main__":
    main()
