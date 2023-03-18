import os
import json
import yaml
import openai

CONFIG_FILE = "config.yaml"

with open(CONFIG_FILE, "r") as f:
    configs = yaml.safe_load(f)

OPEN_API_KEY = configs["OPEN_API_KEY"]
SECRET_KEY = configs["SECRET_KEY"]
PATH_HIST_FOLDER = configs["PATH_HIST_FOLDER"]
MAX_TOKENS = configs["MAX_TOKENS"]
TEMPERATURE = configs["TEMPERATURE"]

openai.api_key = OPEN_API_KEY

def send_request(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # engine="davinci-codex",
        messages=messages,
        # prompt=prompt,              
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    message = response.choices[0].message['content']
    return message.strip()

def load_chat_history(chatname):
    filename = f"{chatname}_hist.txt"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.loads(file.read())
    return []

def save_chat_history(chatname, messages):
    filename = f"{chatname}_hist.txt"
    with open(filename, "w") as file:
        file.write(json.dumps(messages))

if __name__ == "__main__":
    chatname = input("Enter your chatname: ")
    messages = load_chat_history(chatname)

    if messages:
        print(f"Loaded chat history for {chatname}:")
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")

    while True:
        user_input = input("Enter your message (type 'exit' to quit): ")

        if user_input.lower() == 'exit':
            break

        messages.append({"role": "user", "content": user_input})
        response = send_request(messages)
        print("ChatGPT Response:", response)

        messages.append({"role": "assistant", "content": response})
        save_chat_history(chatname, messages)

    print("Conversation history saved.")
