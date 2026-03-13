from fastapi import APIRouter, UploadFile, File, HTTPException
import tempfile
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.get("/")
async def health_check():
    return {"status": "online", "message": "API de Transcrição de Áudio ativa"}

@router.post("/transcrever-audio")
async def transcrever_audio(audio: UploadFile = File(...)):

    extensao = os.path.splitext(audio.filename or "audio.ogg")[1].lower() or ".ogg"
    
    if extensao == ".oga":
        extensao = ".ogg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp:
        conteudo = await audio.read()
        temp.write(conteudo)
        caminho_temp = temp.name

    try:
        with open(caminho_temp, "rb") as arquivo:
            transcricao = client.audio.transcriptions.create(
                model="whisper-1",
                file=arquivo
            )
            print(f"Transcrição completa: {transcricao.text}")
            
        return {
            "texto": transcricao.text
        }
    except Exception as e:
        print(f"Erro na transcrição: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if os.path.exists(caminho_temp):
            os.remove(caminho_temp)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)