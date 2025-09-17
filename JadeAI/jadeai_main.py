# Our main code for the AI

from openai import OpenAI
from dotenv import load_dotenv
import os
import jadeai_instructions

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from jadeai_instructions import name
from jadeai_instructions import personality
from jadeai_instructions import demeanor
from jadeai_instructions import tone
from jadeai_instructions import formality

instructions = " ".join([name, personality, demeanor, tone, formality])


while True:
    user_input = input("Write your text here: ")
    if user_input == "exit":
        print("You have exited!")
        break
    

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_input}
        ]
    )

    print(response.output[0].content[0].text)