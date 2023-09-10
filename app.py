import os
from flask import Flask, request, render_template
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from config import API_KEY, API_URL, ASSISTANT_ID

app = Flask(__name__)

WATSON_API_KEY = API_KEY
WATSON_URL = API_URL
WATSON_ASSISTANT_ID = ASSISTANT_ID

authenticator = IAMAuthenticator(WATSON_API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(WATSON_URL)

def chatWatsonX(text, assistant_id=WATSON_ASSISTANT_ID):
    response = assistant.message(
        assistant_id=assistant_id,
        input={
            'message_type': 'text',
            'text': text
        }
    ).get_result()

    reply = response['output']['generic'][0]['text']
    return reply

@app.route('/', methods=['GET', 'POST'])
def home():
    response = None
    if request.method == 'POST':
        text_to_check = request.form['text_to_check']
        response = chatWatsonX(text_to_check)
    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
