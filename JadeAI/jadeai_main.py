from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import time
import threading

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

sys.path.append("services_keys")
sys.path.append("access_python")
sys.path.append("calender")

import vosksystem_python.speechtotext as stt

thread = threading.Thread(target=stt.listen_loop, daemon=True)
thread.start()

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from ai_python.jadeai_instructions import name, personality, demeanor, tone, formality

from pyttsx3system_python.texttospeech import run_tts

instructions = " ".join([name, personality, demeanor, tone, formality])

print("[JADEAI SYSTEM] Online")

while True:
    if stt.last_sentence:  
        print(f"[JADEAI SYSTEM] Heard: {stt.last_sentence}")
        
        if stt.last_sentence.lower() == "exit":
            print("[JADEAI SYSTEM] You have exited!")
            break

        response = client.responses.create(
            model="gpt-4.1",
            input=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": stt.last_sentence}
            ],
        )

        print("[JADEAI SYSTEM] Detected response")

        stt.listening_enabled = False
        run_tts(response)
        time.sleep(2)
        stt.rec = stt.reset_listener()
        stt.listening_enabled = True

        stt.last_sentence = ""  

    time.sleep(1) 
