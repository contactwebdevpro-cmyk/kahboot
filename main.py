from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
import uuid
from typing import Dict, List
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Kahoot Bot Spawner", version="2.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Stockage des sessions
active_sessions: Dict[str, List[asyncio.Task]] = {}

# === Kahoot Client (à installer : pip install kahoot.py ou vehbiu/kahoot-py) ===
try:
    from kahoot import KahootClient
except ImportError:
    logger.error("Library kahoot non installée. pip install kahoot.py")
    KahootClient = None


async def connect_bot(game_pin: int, name: str, auto_reconnect: bool = False):
    reconnect_count = 0
    max_reconnects = 6

    while reconnect_count < max_reconnects:
        client = KahootClient() if KahootClient else None
        try:
            if not client:
                logger.error("KahootClient non disponible")
                break

            await client.join_game(game_pin=game_pin, username=name)
            logger.info(f"✅ Bot '{name}' connecté au PIN {game_pin}")

            # Rester connecté plus longtemps (Kahoot déconnecte souvent après ~45-60min)
            await asyncio.sleep(2700)  # 45 minutes
            break

        except Exception as e:
            reconnect_count += 1
            logger.warning(f"Bot '{name}' erreur: {e} (tentative {reconnect_count}/{max_reconnects})")
            if auto_reconnect and reconnect_count < max_reconnects:
                await asyncio.sleep(3)
            else:
                break


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/start")
async def start_bots(
    background_tasks: BackgroundTasks,
    game_pin: int = Form(...),
    base_name: str = Form(...),
    nb_bots: int = Form(...),
    auto_reconnect: bool = Form(False)
):
    if not 1 <= nb_bots <= 600:  # Limite raisonnable pour éviter les bans IP
        return JSONResponse({"error": "Nombre de bots entre 1 et 600"}, status_code=400)

    session_id = str(uuid.uuid4())[:8]

    tasks = []
    for i in range(nb_bots):
        name = base_name if i == 0 else f"{base_name}{i+1}"
        task = asyncio.create_task(connect_bot(game_pin, name, auto_reconnect))
        tasks.append(task)

    active_sessions[session_id] = tasks

    return {
        "status": "success",
        "session_id": session_id,
        "message": f"{nb_bots} bots démarrés",
        "count": nb_bots
    }


@app.get("/stop/{session_id}")
async def stop_session(session_id: str):
    if session_id in active_sessions:
        for task in active_sessions[session_id]:
            if not task.done():
                task.cancel()
        del active_sessions[session_id]
        return {"status": "stopped", "message": "Session arrêtée"}
    return {"status": "not_found"}
