import requests
import json

API_KEY = "AIzaSyCN94L68GCs9s9hVOTNysDJHNT3m5YOEFw"
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

def generate_content(user_input):
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_input}]
            }
        ]
    }
    
    response = requests.post(URL, headers=headers, json=data)
    
    if response.status_code == 200:
        response_json = response.json()
        # Ekstrak teks dari respons
        text = response_json['candidates'][0]['content']['parts'][0]['text']
        return text
    else:
        return f"Error: {response.status_code}, {response.text}"

# Loop utama
while True:
    try:
        # Meminta input dari pengguna
        user_input = input("Masukkan pertanyaan atau pernyataan Anda (atau tekan Ctrl+C untuk keluar): ")
        # Memanggil fungsi dan mencetak hasilnya
        result = generate_content(user_input)
        print(result)
        print("\n")  # Menambahkan baris kosong untuk memisahkan setiap interaksi
    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
        break
