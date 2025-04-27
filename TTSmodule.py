import speech_recognition as sr
from flask import jsonify
from gtts import gTTS
import os
def TTS(text) :
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    tts = gTTS(text=text, lang='en')
    file_path = os.path.join('Static/audio', 'output.mp3')
    tts.save(file_path)
    return jsonify({'message': 'Audio file generated'})
