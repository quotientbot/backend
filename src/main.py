from fastapi import FastAPI, Depends, HTTPException
from decouple import config
from fastapi.security import APIKeyHeader
from routes import auth, user, guild
from fastapi.middleware.cors import CORSMiddleware
from utils import http_client

api_scheme = APIKeyHeader(name="authorization")


async def verify_key(key: str = Depends(api_scheme)):
    if key != config("API_KEY"):
        raise HTTPException(status_code=403)


async def on_start_up() -> None:
    http_client.SingletonAiohttp.get_aiohttp_client()


async def on_shutdown() -> None:
    await http_client.SingletonAiohttp.close_aiohttp_client()


app = FastAPI(debug=True, on_startup=[on_start_up], on_shutdown=[on_shutdown])

# dependencies=[Depends(verify_key)]
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(guild.router, prefix="/guild")


origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config("API_HOST"), port=int(config("API_PORT")))
