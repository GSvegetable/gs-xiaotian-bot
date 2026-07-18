import os
import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update, filters
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes

# 小恬的 Token
BOT_TOKEN = "8934477559:AAHv5xchV66sS17-N4Zf5ANNAmD02qT29lg"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ================= 轻量保活网页（防止 Railway 杀后台） =================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Tian is OK')

def run_health_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"🟢 小恬保活已启动 (端口 {port})")
    server.serve_forever()

# ================= 机器人核心逻辑 =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("你好！我是小恬。有事说事，发1拉黑哦。")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    # 只有遇到“在吗”才回复，其他文字一概无视
    if text == "在吗":
        await update.message.reply_text("有事说事看到了会回复别发1发1拉黑")

def main():
    # 启动保活网页（放在后台线程）
    threading.Thread(target=run_health_server, daemon=True).start()

    # 启动机器人
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ 小恬机器人已上线！")
    app.run_polling()

if __name__ == "__main__":
    main()
