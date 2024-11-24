from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .api.api_router import router as main_router
from .helpers.exception_handler import CustomException, http_exception_handler
from app.helpers.database import startDB
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os


async def lifespan(app: FastAPI):
    # Load the ML model
    # client = await startDB()
    # Chèn dữ liệu mặc định sau khi Beanie đã khởi tạo

    yield
    # Clean up the ML models and release the resources
    # client.close()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3001",
    "localhost:3001",
    "http://localhost:4173",
    "localhost:4173",
    "http://frontend:4173",
    "frontend:4173",
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router, prefix="/api")
app.add_exception_handler(CustomException, http_exception_handler)

# Determine the correct path to the web directory
web_dir = os.path.join(os.path.dirname(__file__), "web")

# Ensure the web directory exists
if not os.path.isdir(web_dir):
    os.makedirs(web_dir)

# Mount the web directory to serve static files
app.mount("/web", StaticFiles(directory=web_dir), name="web")
# Mount the web directory to serve static files
# app.mount(
#     "/static", StaticFiles(directory=os.path.join(web_dir, "static")), name="static")
# app.mount(
#     "/themes", StaticFiles(directory=os.path.join(web_dir, "themes")), name="themes")
# app.mount("/img", StaticFiles(directory=os.path.join(web_dir, "img")), name="img")
app.mount("/assets", StaticFiles(directory=os.path.join(web_dir, "assets")), name="assets")

# Serve favicon.ico


@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join(web_dir, "favicon.ico"))


@app.get("/")
async def read_index():
    return FileResponse(os.path.join(web_dir, "index.html"))

# @app.get("/", tags=["root"])
# async def read_root() -> dict:
#     return {"message": "Welcome to FARM Stack."}
