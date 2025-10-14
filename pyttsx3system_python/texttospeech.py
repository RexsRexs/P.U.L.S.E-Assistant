import os
import pyttsx3

print("[PYTTSX3 SYSTEM] Online")

def run_tts(response):
    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
    
    engine = pyttsx3.init()

    # --- RATE ---
    rate = engine.getProperty('rate')
    print("[PYTTSX3 SYSTEM] Current rate:", rate)
    engine.setProperty('rate', 125)

    # --- VOLUME ---
    volume = engine.getProperty('volume')
    print("[PYTTSX3 SYSTEM] Current volume:", volume)
    engine.setProperty('volume', 1.0)

    # --- VOICE ---
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    try:
        text_to_speak = response.output[0].content[0].text
    except Exception as e:
        raise e

    engine.say(text_to_speak)
    engine.runAndWait()
    engine.stop()
