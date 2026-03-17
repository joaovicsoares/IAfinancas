# Usar uma imagem base leve de Python
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Impedir que o Python gere arquivos .pyc e permitir logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema necessárias (se houver)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de dependências
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Expor a porta que a API utiliza
EXPOSE 8000

# Comando para rodar a aplicação usando uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
