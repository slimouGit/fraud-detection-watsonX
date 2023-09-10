import os
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from config import ASSISTANT_ID, API_URL, API_KEY

WATSON_API_KEY = API_KEY
WATSON_URL = API_URL
WATSON_ASSISTANT_ID = ASSISTANT_ID


authenticator = IAMAuthenticator(WATSON_API_KEY)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(API_URL)

# Sitzung initialisieren
session_id = None

try:
    # Sitzung erstellen
    session_response = assistant.create_session(
        assistant_id=WATSON_ASSISTANT_ID
    ).get_result()

    # session_id aus der Antwort extrahieren
    session_id = session_response['session_id']

    # Testanfrage an Watson Assistant mit der Sitzung
    response = assistant.message(
        assistant_id=WATSON_ASSISTANT_ID,
        session_id=session_id,  # Verwenden Sie die session_id hier
        input={
            'message_type': 'text',
            'text': 'Hello, Watson!'
        }
    ).get_result()

    # Überprüfen, ob die Anfrage erfolgreich war
    if 'output' in response and 'generic' in response['output']:
        print("Ihre Konfiguration ist valide. Eine Verbindung zum Watson Assistant wurde erfolgreich hergestellt.")
    else:
        print("Ihre Konfiguration ist möglicherweise nicht korrekt. Bitte überprüfen Sie Ihre API-Key, URL und Assistant-ID.")

finally:
    if session_id:
        # Sitzung beenden, um Ressourcen freizugeben, falls eine Sitzung erstellt wurde
        assistant.delete_session(
            assistant_id=WATSON_ASSISTANT_ID,
            session_id=session_id
        )
