import pymongo
import sys
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from pymongo.server_api import ServerApi

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

client = pymongo.MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi('1'))
database = client["ai_memory"]

user = "user"
role = "assistant"

conversations = database["conversations"]
def save_conversation(user, role, response):
    conversations.insert_one({
        "user_id": user,
        "role": role,
        "content": response,
        "timestamp": datetime.utcnow()
    })

def get_conversation_history(user_id, limit=10):
    messages = list(conversations.find(
        {"user_id": user_id},
        {"_id": 0, "role": 1, "content": 1} 
    ).sort("timestamp", -1).limit(limit))
    
    return list(reversed(messages))

user_knowledge = database["user_knowledge"]
def save_user_knowledge(user, key, value):
    user_knowledge.update_one(
        {"user_id": user},
        {"$set": {f"facts.{key}": value}},
        upsert=True
    )

def get_user_knowledge(user):
    data = user_knowledge.find_one({"user_id": user})
    return data.get("facts", {}) if data else {}

def extract_knowledge(user_id, recent_messages):
    conv_text = "\n".join([f"{m['role']}: {m['content']}" for m in recent_messages])
    
    extraction_prompt = f"""Analyze this conversation and extract ONLY important facts about the user.
Only include facts that are:
- Personal (name, age, location, job, etc.)
- Preferences (likes, dislikes, hobbies)
- Important context the AI should remember

Return as simple key:value pairs, one per line. Example:
name: John
location: Denmark
job: software developer

If no important facts, return "none".

Conversation:
{conv_text}"""
    
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": extraction_prompt}]
    )
    
    facts_text = response.choices[0].message.content.strip()
    
    if facts_text.lower() != "none":
        for line in facts_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                save_user_knowledge(user_id, key.strip(), value.strip())