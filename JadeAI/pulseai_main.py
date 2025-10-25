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

from ai_python.pulseai_instructions import name, personality, demeanor, tone, formality, primary_objectives, communication_style, capabilities

from pyttsx3system_python.texttospeech import run_tts

from database_python.mongodb_database_jadeai import save_conversation, get_conversation_history, extract_knowledge, conversations

instructions = " ".join([name, personality, demeanor, tone, formality, primary_objectives, communication_style, capabilities])

print("[P.U.L.S.E SYSTEM] Online")
while True:
    if stt.last_sentence:  
        print(f"[P.U.L.S.E SYSTEM] Heard: {stt.last_sentence}")
        
        if stt.last_sentence.lower() == "exit":
            print("[P.U.L.S.E SYSTEM] You have exited!")
            break

        history = get_conversation_history("user123", limit=10)

        messages = [{"role": "system", "content": instructions}]
        messages.extend(history) 
        messages.append({"role": "user", "content": stt.last_sentence})
 
        response = client.responses.create(
        model="gpt-4.1",
        input=messages,
        )

        user_message = stt.last_sentence
        response_text = response.output[0].content[0].text

        print("[P.U.L.S.E SYSTEM] Detected response")

        save_conversation("user123", "user", user_message)
        save_conversation("user123", "assistant", response_text)
        
        message_count = conversations.count_documents({"user_id": "user123"})
        if message_count % 10 == 0: 
            recent_messages = get_conversation_history("user123", limit=10)
            extract_knowledge("user123", recent_messages)

        stt.listening_enabled = False
        run_tts(response)
        time.sleep(2)
        stt.rec = stt.reset_listener()
        stt.listening_enabled = True

        stt.last_sentence = ""  

    time.sleep(1) 
