from fastapi import FastAPI
import uvicorn
from interpretarTexto import router as interpretar_router
from transcreverAudio import router as transcrever_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="IA Finanças - API Consolidada")

# Incluindo os roteadores das outras funcionalidades
app.include_router(interpretar_router)
app.include_router(transcrever_router)

@app.get("/health")
async def root_health():
    return {"status": "online", "message": "API Central IA Finanças ativa"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
