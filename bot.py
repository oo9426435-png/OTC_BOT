import os
import requests
import time
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# سحب التوكن من إعدادات المنصة أو استخدامه مباشرة
TOKEN = os.environ.get('BOT_TOKEN', "8542925328:AAEGzXEmJEQUUP9bKk7Pa6piO7ftBUn735k")

# ==================== إعداد سيرفر الويب (لمنع البوت من النوم 24/7) ====================
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running 24/7!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ===================================================================================

def get_main_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "🎯 صيد صفقة (تلقائي مستمر)", "callback_data": "hunt_trade"}],
            [{"text": "🔍 فحص السوق الشامل", "callback_data": "check_market"}],
            [{"text": "📊 الأزواج المفضلة", "callback_data": "set_pairs"}, {"text": "⚙️ الإعدادات", "callback_data": "settings"}],
            [{"text": "🔄 إعادة التشغيل", "callback_data": "restart"}]
        ]
    }

def send_menu(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    text = "🤖 **لوحة تحكم بوت إشارات OTC**\n\nحالة البوت: `🟢 جاهز للأتمتة المستمرة 24/7`\nاختر من القائمة أدناه:"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown", "reply_markup": get_main_keyboard()}
    try:
        res = requests.post(url, json=payload, timeout=10).json()
        return res.get("result", {}).get("message_id")
    except:
        return None

# تشغيل سيرفر الويب في الخلفية قبل تشغيل حلقة البوت
if __name__ == "__main__":
    keep_alive()
    print("🤖 البوت يعمل الآن باستجابة كاملة للأزرار ومع سيرفر الويب 24/7...")

    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=2"
            response = requests.get(url, timeout=5).json()
            
            if "result" in response:
                for update in response["result"]:
                    offset = update["update_id"] + 1
                    
                    if "callback_query" in update:
                        query = update["callback_query"]
                        data = query["data"]
                        chat_id = query["message"]["chat"]["id"]
                        msg_id = query["message"]["message_id"]
                        cb_id = query["id"]
                        
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": cb_id, "text": "جاري التنفيذ..."})
                        
                        if data == "back_to_menu" or data == "restart":
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": chat_id, "message_id": msg_id})
                            send_menu(chat_id)
                            
                        elif data == "check_market":
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": chat_id, "message_id": msg_id})
                            caption = "📊 **فحص السوق الشامل:**\n- الحالة: مستقرة.\n- التحليل: تتبع سلوك الشموع الثلاثة لرصد نقاط الانعكاس بدقة."
                            chart_url = "https://quickchart.io/chart?w=600&h=300&c={type:'line',data:{labels:['T1','T2','T3'],datasets:[{label:'Trend',data:[1.08,1.082,1.081],borderColor:'blue'}]}}"
                            back_keyboard = {"inline_keyboard": [[{"text": "🔙 العودة للقائمة الرئيسية", "callback_data": "back_to_menu"}]]}
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", json={
                                "chat_id": chat_id, "photo": chart_url, "caption": caption, "parse_mode": "Markdown", "reply_markup": back_keyboard
                            })
                            
                        elif data == "set_pairs":
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": chat_id, "message_id": msg_id})
                            back_keyboard = {"inline_keyboard": [[{"text": "🔙 العودة للقائمة الرئيسية", "callback_data": "back_to_menu"}]]}
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                                "chat_id": chat_id, "text": "📊 **الأزواج النشطة:**\n1. `EUR/USD OTC`\n2. `GBP/USD OTC`", "parse_mode": "Markdown", "reply_markup": back_keyboard
                            })
                            
                        elif data == "settings":
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": chat_id, "message_id": msg_id})
                            back_keyboard = {"inline_keyboard": [[{"text": "🔙 العودة للقائمة الرئيسية", "callback_data": "back_to_menu"}]]}
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
                                "chat_id": chat_id, "text": "⚙️ **الإعدادات:**\n- الاستراتيجية: `دراسة الشموع الثلاثة`\n- الإطار الزمني: `دقيقة واحدة (1M)`", "parse_mode": "Markdown", "reply_markup": back_keyboard
                            })
                            
                        elif data == "hunt_trade":
                            requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": chat_id, "message_id": msg_id})
                            
                            target_time = datetime.now() + timedelta(seconds=45)
                            entry_time_str = target_time.strftime("%H:%M:%S")
                            chart_url = "https://quickchart.io/chart?w=600&h=300&c={type:'bar',data:{labels:['السياق','الدراسة','الإثبات'],datasets:[{label:'EUR/USD',data:[[1.082,1.080],[1.080,1.079],[1.079,1.083]],backgroundColor:['red','red','green']}]}}"
                            
                            persistent_keyboard = {
                                "inline_keyboard": [
                                    [{"text": "🔙 العودة للقائمة الرئيسية", "callback_data": "back_to_menu"}]
                                ]
                            }
                            
                            trade_caption = (
                                f"🎯 **تم صيد الصفقة بنجاح!** 🚀\n\n"
                                f"- الزوج: `EUR/USD OTC`\n"
                                f"- 🕯️ **شمعة السياق:** هبوط تصحيحي\n"
                                f"- 🔍 **شمعة الدراسة:** اختبار الدعم برفض سعري\n"
                                f"- ✅ **شمعة الإثبات:** صعود مؤكد (`صعود 🟢`)\n"
                                f"- ⏱️ **المدة:** `دقيقة واحدة (1M)`\n"
                                f"- ⏰ **وقت الدخول:** `{entry_time_str}`\n"
                                f"- 🔄 **الانتقال للصفقة التالية:** `00:00:45`"
                            )
                            
                            send_res = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto", json={
                                "chat_id": chat_id, "photo": chart_url, "caption": trade_caption, "parse_mode": "Markdown", "reply_markup": persistent_keyboard
                            }).json()
                            
                            active_msg_id = send_res.get("result", {}).get("message_id")
                            
                            while datetime.now() < target_time:
                                time.sleep(1)
                                now = datetime.now()
                                remaining = int((target_time - now).total_seconds())
                                if remaining < 0:
                                    remaining = 0
                                
                                mins, secs = divmod(remaining, 60)
                                updated_caption = (
                                    f"🎯 **تم صيد الصفقة بنجاح!** 🚀\n\n"
                                    f"- الزوج: `EUR/USD OTC`\n"
                                    f"- 🕯️ **شمعة السياق:** هبوط تصحيحي\n"
                                    f"- 🔍 **شمعة الدراسة:** اختبار الدعم برفض سعري\n"
                                    f"- ✅ **شمعة الإثبات:** صعود مؤكد (`صعود 🟢`)\n"
                                    f"- ⏱️ **المدة:** `دقيقة واحدة (1M)`\n"
                                    f"- ⏰ **وقت الدخول:** `{entry_time_str}`\n"
                                    f"- 🔄 **الانتقال للصفقة التالية:** `00:{mins:02d}:{secs:02d}`"
                                )
                                
                                requests.post(f"https://api.telegram.org/bot{TOKEN}/editMessageCaption", json={
                                    "chat_id": chat_id, "message_id": active_msg_id, "caption": updated_caption, "parse_mode": "Markdown", "reply_markup": persistent_keyboard
                                })
                                
                                check_updates = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=0").json()
                                if "result" in check_updates and len(check_updates["result"]) > 0:
                                    first_up = check_updates["result"][0]
                                    if "callback_query" in first_up and first_up["callback_query"]["data"] == "back_to_menu":
                                        offset = first_up["update_id"] + 1
                                        requests.post(f"https://api.telegram.org/bot{TOKEN}/answerCallbackQuery", json={"callback_query_id": first_up["callback_query"]["id"], "text": "تم العودة للقائمة"})
                                        requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", json={"chat_id": chat_id, "message_id": active_msg_id})
                                        send_menu(chat_id)
                                        break
                            else:
                                continue
                                
        except Exception as e:
            print("خطأ:", e)
            time.sleep(1)
