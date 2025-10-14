import sys
import os
import sounddevice as sd
import queue
import json
import time
from vosk import Model, KaldiRecognizer

BASE_STT = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_STT, "vosk-model-small-en-us-0.15")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

model = Model(MODEL_PATH)

samplerate = 16000
q = queue.Queue()

last_sentence = ""  

def callback(indata, frames, time_, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def listen_loop(timeout=5):
    """
    Starter Vosk-lytning med en timeout, men stopper ikke programmet.
    """
    global last_sentence, listening_enabled
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        print("[VOSK SYSTEM] Online")

        rec = KaldiRecognizer(model, samplerate)
        start_time = time.time()

        while True:
            if not listening_enabled:
                time.sleep(0.1)
                continue

            try:
                data = q.get(timeout=timeout)
            except queue.Empty:
                start_time = time.time()
                continue

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").strip()
                if text:
                    last_sentence = text
                    print("[VOSK SYSTEM]", last_sentence)
                    start_time = time.time()
            else:
                partial = json.loads(rec.PartialResult())
                if partial.get("partial"):
                    print("[VOSK SYSTEM] Hearing:", partial["partial"])

def reset_listener():
    """
    Tøm køen og genstart recognizer, så gamle lyde ikke fanges.
    """
    global q, model
    while not q.empty():
        q.get_nowait()

    rec = KaldiRecognizer(model, samplerate)
    return rec


listening_enabled = True

if __name__ == "__main__":
    listen_loop()