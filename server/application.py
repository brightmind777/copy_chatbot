from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS

import TTSmodule

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Get the OpenAI API key from environment variables
api_key = os.getenv('DEEPSEEK_API_KEY')

def chat_with_openai(message):
    url = 'https://api.deepseek.com/chat/completions'
    headers = {
        'accept' : '*/*',
        'content-type' : 'application/json',
        'origin': 'https://gen-ai-chat-app-git-main-mrblackghostts-projects.vercel.app',
        'referer' : 'https://gen-ai-chat-app-git-main-mrblackghostts-projects.vercel.app/',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    }
    payload = {"contents":[{"parts":[{"text":message}]}],"persona":"Piyush"}

    response = requests.post('https://gen-ai-chat-app-git-main-mrblackghostts-projects.vercel.app/api/chat', json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data['candidates'][0]['content']['parts'][0]['text'])
        return data['candidates'][0]['content']['parts'][0]['text']
    
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = chat_with_openai(user_message)
        return jsonify({'reply': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file)

    with audio_data as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'error': 'Speech Recognition could not understand audio'}), 400
        except sr.RequestError as e:
            return jsonify({'error': f'Could not request results; {e}'}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.json.get('text')
    return TTSmodule.TTS(text)
if __name__ == '__main__':
    app.run(debug=True)
