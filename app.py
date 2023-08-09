from flask import Flask, render_template, request, jsonify
import openai
from config import API_KEY
from prompt import PROMPT

app = Flask(__name__)

openai.api_key = API_KEY
global_prompt = PROMPT

def chatGPT(text, temperature=0.7):
    messages = [{"role": "system", "content": "You are a fraud detection assistant."}]
    messages.append({"role": "user", "content": global_prompt + text})
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=temperature
    )
    reply = chat.choices[0].message['content']
    return reply

@app.route('/', methods=['GET', 'POST'])
def home():
    response = None
    if request.method == 'POST':
        text_to_check = request.form['text_to_check']
        response = chatGPT(text_to_check, temperature=0.8)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
