from typing import Tuple

import uvicorn
from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware

from database import Base, engine
from endpoints.article_sql import router as article_router
from endpoints.comment_sql import router as comment_router
from endpoints.profile_sql import router as profile_router
from endpoints.tag_sql import router as tag_router
from endpoints.user_sql import router as user_router
# from endpoints import dateparser

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


@app.on_event("startup")
async def startup():
    # Créer les tables au démarrage de l'application
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(user_router, tags=["user"])
app.include_router(article_router, tags=["article"])
app.include_router(comment_router, tags=["article"])
app.include_router(tag_router, tags=["tag"])
app.include_router(profile_router, tags=["profile"])
# app.include_router(dateparser.router, prefix="/api", tags=["DateParser"])

if __name__ == "__main__":
    uvicorn.run(app)
