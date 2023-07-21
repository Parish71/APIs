

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configurações da API e escopos
CLIENT_FILE = 'account.1.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Autenticação com a API
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Construção do objeto de serviço para a API do Gmail
service_gmail = build('gmail', 'v1', credentials=creds)

# Criar e enviar uma mensagem
def create_message(sender, to, subject, message_text):
    message = {
        'raw': base64.urlsafe_b64encode(f"From: {sender}\nTo: {to}\nSubject: {subject}\n\n{message_text}".encode("utf-8")).decode("utf-8")
    }
    return message

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print("E-mail enviado com sucesso! Mensagem ID:", message['id'])
        return message
    except Exception as e:
        print("Ocorreu um erro ao enviar o e-mail:", str(e))

# Enviar e-mail
sender_email = "rafaelfparish@gmail.com"  # Substitua pelo seu e-mail
recipient_email = "rafaelfparish@gmail.com"  # Substitua pelo endereço de e-mail do destinatário
subject = "Hello World"
message_text = "Hello World! This is a test email sent using the Gmail API."

message = create_message(sender_email, recipient_email, subject, message_text)
send_message(service_gmail, "me", message)