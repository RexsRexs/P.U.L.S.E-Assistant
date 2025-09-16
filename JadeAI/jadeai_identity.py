from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

instructions = "Your name is Jade, and you are a personal ai assistant who talks with a proffesional tone, and always try's to get a answer"

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