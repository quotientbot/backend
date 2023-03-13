from fastapi import FastAPI, Depends, HTTPException
from decouple import config
from fastapi.security import APIKeyHeader
from .routes import auth, user, guild
from fastapi.middleware.cors import CORSMiddleware
from .utils import http_client
from tortoise.contrib.fastapi import register_tortoise
from .settings import TORTOISE_CONF

# from fastapi_health import health


api_scheme = APIKeyHeader(name="authorization")


async def verify_key(key: str = Depends(api_scheme)):
    if key != config("API_KEY"):
        raise HTTPException(status_code=403)


async def on_start_up() -> None:
    http_client.SingletonAiohttp.get_aiohttp_client()


async def on_shutdown() -> None:
    await http_client.SingletonAiohttp.close_aiohttp_client()


# def pass_condition():
#     return {"database": "online"}


# def sick_condition():
#     return False


app = FastAPI(debug=True, on_startup=[on_start_up], on_shutdown=[on_shutdown])
# app.add_api_route("/health", health([pass_condition, sick_condition]))


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


# register_tortoise(
#     app,
#     config=TORTOISE_CONF,
#     generate_schemas=True,
#     add_exception_handlers=True,
# )
