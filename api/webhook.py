import os
import json
from http.server import BaseHTTPRequestHandler
import urllib.request

TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "")

TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"


def send_message(chat_id, text, reply_to_message_id=None):
    url = f"{TELEGRAM_API}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    if reply_to_message_id:
        payload["reply_to_message_id"] = reply_to_message_id
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)


def forward_message(from_chat_id, message_id):
    url = f"{TELEGRAM_API}/forwardMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "from_chat_id": from_chat_id,
        "message_id": message_id,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)


def set_webhook(webhook_url):
    url = f"{TELEGRAM_API}/setWebhook"
    payload = {"url": webhook_url}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode("utf-8"))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            update = json.loads(body)

            message = update.get("message", {})
            chat_id = message.get("chat", {}).get("id")
            text = message.get("text", "")
            message_id = message.get("message_id")
            has_photo = "photo" in message
            has_document = "document" in message

            if chat_id and text == "/start":
                send_message(
                    chat_id,
                    "أهلاً بك في بوت قناة Min Al-Sifr Tech! 🚀\n"
                    "أرسل لي سكرين شوت أو صورة الإيموجيز المخفية للمشاركة في السحب.",
                    reply_to_message_id=message_id,
                )
            elif chat_id and (has_photo or has_document):
                try:
                    forward_message(chat_id, message_id)
                    send_message(
                        chat_id,
                        "تم استلام الصورة بنجاح! 🎯 بالتوفيق في الجيف أواي.",
                        reply_to_message_id=message_id,
                    )
                except Exception:
                    send_message(
                        chat_id,
                        "عذراً، حدث خطأ أثناء الإرسال. تأكد من إرسال الصورة بشكل صحيح.",
                        reply_to_message_id=message_id,
                    )
        except Exception:
            pass

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        path = self.path

        if path.startswith("/api/set_webhook"):
            host = self.headers.get("Host", "")
            webhook_url = f"https://{host}/api/webhook"
            try:
                result = set_webhook(webhook_url)
                response = json.dumps(result).encode("utf-8")
            except Exception as e:
                response = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write("Bot is running! 🚀".encode("utf-8"))
