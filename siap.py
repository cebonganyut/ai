import requests
import json
import time

# Fungsi untuk menerima notifikasi
def receive_notification():
    url = "https://7103.api.greenapi.com/waInstance7103961704/receiveNotification/8b2659c3a610483487dcba3bd67d101470ca098a8dcb483bae"
    response = requests.get(url)
    return response.json()

# Fungsi untuk menghapus notifikasi
def delete_notification(receipt_id):
    url = f"https://7103.api.greenapi.com/waInstance7103961704/deleteNotification/8b2659c3a610483487dcba3bd67d101470ca098a8dcb483bae/{receipt_id}"
    requests.delete(url)

# Fungsi untuk generate konten menggunakan API Gemini
def generate_content(user_input):
    api_key = "AIzaSyCN94L68GCs9s9hVOTNysDJHNT3m5YOEFw"
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_input}]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        return text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Fungsi untuk mengirim pesan WhatsApp
def send_whatsapp_message(chat_id, message):
    url = "https://7103.api.greenapi.com/waInstance7103961704/sendMessage/8b2659c3a610483487dcba3bd67d101470ca098a8dcb483bae"
    payload = {
        "chatId": chat_id,
        "message": message
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Main loop
while True:
    notification = receive_notification()
    
    if notification is not None and 'body' in notification:
        body = notification['body']
        
        if body['typeWebhook'] == 'incomingMessageReceived':
            chat_id = body['senderData']['sender']
            if 'messageData' in body and 'extendedTextMessageData' in body['messageData']:
                user_input = body['messageData']['extendedTextMessageData']['text']
                
                # Generate response
                response = generate_content(user_input)
                
                # Send response back to WhatsApp
                send_result = send_whatsapp_message(chat_id, response)
                print(f"Sent message: {send_result}")
        
        # Delete the processed notification
        delete_notification(notification['receiptId'])
    
    time.sleep(1)  # Wait for 1 second before checking for new notifications
