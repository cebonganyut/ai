import os
import time
import requests
import logging
from whatsapp_bot import WhatsAppBot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Gemini API Configuration
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    logging.error("GEMINI_API_KEY not set in environment variables.")
    exit(1)

URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

def generate_content(user_input):
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_input}]
            }
        ]
    }
    
    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for HTTP error codes
        
        response_json = response.json()
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        return text
    except requests.RequestException as e:
        logging.error(f"Error in API request: {e}")
        return "Maaf, terjadi kesalahan saat memproses permintaan Anda."
    except (KeyError, IndexError) as e:
        logging.error(f"Error parsing API response: {e}")
        return "Maaf, terjadi kesalahan saat memproses respons."

# Initialize WhatsApp bot
bot = WhatsAppBot()

logging.info("Silakan scan QR Code untuk login ke WhatsApp Web")
bot.wait_for_login()
logging.info("Login berhasil!")

@bot.message_handler(pattern=".*")
def reply_to_message(message):
    logging.info(f"Menerima pesan: {message.content}")
    response = generate_content(message.content)
    logging.info(f"Mengirim balasan: {response}")
    message.reply(response)

logging.info("Bot siap menerima pesan...")
bot.start()

# Keep the script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Mematikan bot...")
    bot.stop()
