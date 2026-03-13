from fastapi import APIRouter
from openai import OpenAI
import os
from dotenv import load_dotenv
router = APIRouter()

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/interpretar-transacao")
async def interpretar_transacao(payload: dict):

    texto = payload["texto"]

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
Extraia os dados financeiros do texto.

Retorne apenas JSON com:

tipo
valor
categoria
descricao
data
"""
            },
            {
                "role": "user",
                "content": texto
            }
        ]
    )

    return resposta.choices[0].message.content