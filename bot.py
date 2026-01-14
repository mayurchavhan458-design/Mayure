from flask import Flask, render_template_string, request, jsonify
from telethon import TelegramClient, sync
import time
import re

app = Flask(__name__)

# --- TERI DETAILS ---
API_ID = 38211053
API_HASH = '4bd24e08363166af9aedaf1cbdd61644'
CHAT_ID = -1003656764880  

client = TelegramClient('premium_session', API_ID, API_HASH)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #020617; font-family: 'Segoe UI', sans-serif; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 30px; border-radius: 20px; border: 1px solid #3b82f6; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 0 25px rgba(59, 130, 246, 0.3); }
        h2 { color: #3b82f6; text-transform: uppercase; letter-spacing: 2px; }
        input { width: 100%; padding: 15px; margin: 15px 0; border-radius: 12px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; outline: none; }
        .btn { width: 100%; padding: 16px; border-radius: 12px; border: none; background: linear-gradient(90deg, #2563eb, #1d4ed8); color: white; font-weight: bold; cursor: pointer; }
        .result-box { background: #064e3b; padding: 15px; border-radius: 12px; margin-top: 20px; word-break: break-all; border: 1px solid #10b981; }
        .open-btn { background: #10b981; margin-top: 15px; text-decoration: none; display: block; padding: 15px; border-radius: 12px; color: white; font-weight: bold; }
        .error-box { background: #450a0a; padding: 10px; border-radius: 10px; margin-top: 10px; font-size: 12px; color: #fca5a5; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Premium Bypasser</h2>
        <input type="text" id="targetUrl" placeholder="Paste Link Here...">
        <button class="btn" onclick="sendRequest()">BYPASS NAME</button>
        <div id="status"></div>
    </div>

    <script>
        async function sendRequest() {
            const url = document.getElementById('targetUrl').value;
            const status = document.getElementById('status');
            if(!url) return alert("Bhai link dalo!");
            
            status.innerHTML = "⏳ Wait... Bot se link nikaal raha hoon...";
            
            try {
                const response = await fetch('/get_key', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: url })
                });
                const data = await response.json();
                
                if(data.success) {
                    status.innerHTML = `
                        <div class="result-box">
                            <b>Bypassed Link:</b><br>${data.link}
                        </div>
                        <a href="${data.link}" target="_blank" class="open-btn">OPEN LINK</a>
                    `;
                } else {
                    status.innerHTML = `
                        <div class="result-box" style="background:#7f1d1d; border-color:#ef4444;">
                            ${data.message}
                        </div>
                        <div class="error-box"><b>Bot Message:</b> ${data.raw_text || "No message captured"}</div>
                    `;
                }
            } catch (e) {
                status.innerHTML = "❌ Connection Error!";
            }
        }
    </script>
</body>
</html>
'''

def extract_link(text):
    # Sabse strong regex jo har tarah ke link ko pakad lega
    url_pattern = r'(https?://[^\s<>"]+|www\.[^\s<>"]+)'
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_key', methods=['POST'])
def get_key():
    url = request.json.get('url')
    try:
        if not client.is_connected():
            client.connect()
        
        # Link bhej rahe hain
        client.send_message(CHAT_ID, url)
        
        # Wait time 15 second kar diya taaki bot ko pura mauka mile
        time.sleep(15)
        
        # Latest message
        messages = client.get_messages(CHAT_ID, limit=1)
        
        if messages:
            bot_text = messages[0].text
            # Hum link nikalne ki koshish karenge
            final_link = extract_link(bot_text)
            
            if final_link:
                return jsonify({"success": True, "link": final_link})
            else:
                # Agar link nahi mila toh pura text wapas bhejenge debugging ke liye
                return jsonify({"success": False, "message": "Bot ne reply toh diya par link nahi mila!", "raw_text": bot_text})
        else:
            return jsonify({"success": False, "message": "Bot ne koi reply hi nahi diya!"})
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

if __name__ == '__main__':
    client.start() 
    print("✅ Bypasser Ready!")
    app.run(host='0.0.0.0', port=5000, threaded=False)
