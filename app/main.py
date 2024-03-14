from fastapi import FastAPI
from app.api import endpoints


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(endpoints.router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
