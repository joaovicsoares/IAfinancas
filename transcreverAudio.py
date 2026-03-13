from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/transcrever-audio")
async def transcrever_audio(audio: UploadFile = File(...)):
    extensao = os.path.splitext(audio.filename or "audio.ogg")[1] or ".ogg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp:
        conteudo = await audio.read()
        temp.write(conteudo)
        caminho_temp = temp.name

    try:
        with open(caminho_temp, "rb") as arquivo:
            transcricao = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=arquivo
            )

        return {
            "texto": transcricao.text
        }
    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)