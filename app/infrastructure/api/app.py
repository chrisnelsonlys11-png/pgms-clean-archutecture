from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.infrastructure.database.connection import Base, engine
from app.infrastructure.api.routes import router

app = FastAPI(title="PGMS", version="1.0.0")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


init_db()
app.include_router(router)


@app.exception_handler(ValueError)
async def value_error_handler(_, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "PGMS API is running successfully",
        "status": "active",
    }
