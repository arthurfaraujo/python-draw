import smtplib
from email.message import EmailMessage
import random
from getpass import getpass
import pickle
import os
from typing import Any

def load_pickle_file(filename: str) -> Any | None:
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "rb") as f:
            return pickle.load(f)
    return None

credentials: dict[str, str] | None = load_pickle_file("credentials")
participants: list[dict[str, str]] | None = load_pickle_file("participants")
qtt_participants: int = 0

if credentials is None:
    myemail = input("Digite o seu email: ")
    password = getpass("Digite a senha de app do seu email: ")

    with open("credentials", "wb") as f:
        pickle.dump({
            "email": myemail,
            "password": password
        }, f)
    
    credentials = {"email": myemail, "password": password}
    
if participants is None:
    qtt_participants = int(input('Quantos participantes serão? '))
    participants = []

    for i in range(qtt_participants):
        name = input('Nome: ')
        email = input('Email: ')
        participants.append({"name": name, "email": email})

    with open("participants", "wb") as f:
        pickle.dump(participants, f)

input('Pressione enter para sortear: ')

for idx, participant in enumerate(participants):
    participants.pop(idx)
    participant['draw'] = random.choice(participants)['name']
    participants.insert(idx, participant)

    msg = EmailMessage()
    msg['Subject'] = 'Sorteio do amigo secreto'
    msg['To'] = participant['email']
    msg.set_content(f'Seu amigo secreto é: {participant["draw"]}')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(credentials["email"], credentials["password"])
        smtp.send_message(msg)
