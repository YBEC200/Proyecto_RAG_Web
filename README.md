# RAG Chatbot - Corporación CDT

Microservicio de IA especializado en consultas de productos de hardware.

## Requisitos

- Python 3.13+
- pip / uv

## Instalación

1. Crear entorno virtual:

```bash
python -m venv .venv
```

2. Activar entorno:

```bash
# Windows (Git Bash / PowerShell)
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r pyproject.toml
# o
uv sync
```

## Configuración

Crear archivo `.env` en la raíz:

```env
APP_NAME=chatlog-api
APP_ENV=local

OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini

GROQ_API_KEY=gsk_...

LARAVEL_API_BASE=http://127.0.0.1:8000/api
LARAVEL_API_TOKEN=2|<token_de_laravel>

DEBUG=true
```

## Ejecución

Desde la raíz del proyecto:

```bash
# Activar entorno
.venv\Scripts\activate

# Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

El RAG estará disponible en `http://127.0.0.1:8001`

## Endpoints

### POST `/chat/`

Procesa pregunta del usuario.

**Request:**

```json
{
  "message": "¿Qué tarjetas gráficas tienen disponible?"
}
```

**Response:**

```json
{
  "answer": "Tenemos disponibles tarjetas Ryzen 5600..."
}
```

**Nota:** No requiere autenticación (el RAG usa credenciales de `.env` para conectar a Laravel)

## Arquitectura

- **Frontend** → conecta directo a RAG (`:8001`)
- **RAG** → consulta Laravel en background para obtener datos de productos
- **Laravel** → API de datos (productos, stock, etc.)

Esta arquitectura **evita deadlocks** entre Laravel y RAG.

## Logs

En la consola de uvicorn verás:

- `🔄 Cargando productos...` - Startup precargando catálogo
- `✅ Índice FAISS construido` - Índice listo para búsquedas
- Requests y respuestas del chat

MIO:
Siempre activa el entorno virtual:
source .venv/Scripts/activate
python -m uv run uvicorn app.main:app --port 8001
