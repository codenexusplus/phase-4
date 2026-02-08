from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.chat_endpoint_absolute import router as chat_router
from api.task_endpoint import router as task_router
from api.auth_endpoint import router as auth_router
from config.settings import settings
from database.connection import async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Initialize database tables if needed
    # await create_tables()  # Uncomment if you have a function to create tables

    yield

    # Shutdown
    await async_engine.dispose()


app = FastAPI(
    title="AI Todo Agentic System",
    description="An AI-powered todo management system with natural language processing",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chat router
app.include_router(chat_router, prefix="/api", tags=["chat"])

# Include the task router
app.include_router(task_router, prefix="/api", tags=["tasks"])

# Include the auth router
app.include_router(auth_router, prefix="/api", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Todo Agentic System!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
