from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
app = FastAPI(
    title="FastAPI Demo",
    description="A FastAPI application with Docker and Poetry",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"Moonshot Server is running 🚀"}

@app.get("/health")
async def health_check():
    return f"Healthy {time.time()}"