import requests
import json

# Function to generate content using the Gemini API
def generate_content(user_input):
    api_key = "AIzaSyCN94L68GCs9s9hVOTNysDJHNT3m5YOEFw"
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_input}]
            }
        ]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return "Error accessing Gemini API"
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

# Function to send a WhatsApp message using GreenAPI
def send_whatsapp_message(to, message):
    url = "https://7103.api.greenapi.com/waInstance7103961704/sendMessage/8b2659c3a610483487dcba3bd67d101470ca098a8dcb483bae"
    data = {
        'chatId': f'{to}@c.us',
        'message': message
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        return "Error sending WhatsApp message"
    return response.json()

# Flask app to handle webhooks (assuming you're using Flask)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    input_data = request.json
    if 'body' in input_data and 'messageData' in input_data['body'] and 'textMessageData' in input_data['body']['messageData']:
        from_user = input_data['body']['senderData']['sender']
        message = input_data['body']['messageData']['textMessageData']['textMessage']
        
        # Generate response
        response = generate_content(message)
        
        # Send response
        result = send_whatsapp_message(from_user, response)
        if 'idMessage' in result:
            return jsonify({"message": f"Message sent with ID: {result['idMessage']}"})
        else:
            return jsonify({"error": f"Error sending message: {json.dumps(result)}"})
    else:
        return jsonify({"error": "Not a text message or unrecognized format"})

if __name__ == '__main__':
    app.run(debug=True)
