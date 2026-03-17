from fastapi import APIRouter
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

router = APIRouter()

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/interpretar-transacao")
async def interpretar_transacao(payload: dict):

    texto = payload["texto"]
    hoje = datetime.now().strftime("%Y-%m-%d")

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"""
Extraia os dados financeiros do texto.
A data de hoje é {hoje}. Use esta referência para datas relativas como 'hoje', 'ontem', etc.

Retorne apenas JSON com:

categoryId: '', -- sempre '0b91460d-d079-4177-b287-6ec6f191960d'
sharedWalletId: null, -- sempre null
amount: 0.00, -- valor sempre positivo
type: 1, -- 1 = despesa, 0 = receita
recurrenceType: 0, -- 0 = única, 1 = fixa, 2 = parcelada
totalInstallments: null, -- apenas preencher se recurrenceType = 2
description: '', -- máximo 200 caracteres
date: '' -- informe data e hora em UTC no formato ISO 8601 yyyy-MM-ddTHH:mm:ssZ
"""
            },
            {
                "role": "user",
                "content": texto
            }
        ]
    )

    content = resposta.choices[0].message.content
    
    # Remove markdown formatting if present
    if content.startswith("```json"):
        content = content.replace("```json", "").replace("```", "").strip()
    elif content.startswith("```"):
        content = content.replace("```", "").strip()
        
    import json
    return json.loads(content)