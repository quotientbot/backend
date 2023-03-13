from fastapi import APIRouter

from ..utils import http_client
from decouple import config
import typing as T

__all__ = ("router",)
router = APIRouter()


async def exchange_code(code: str) -> dict:
    """
    Exchange the code for user's access token
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": config("DISCORD_CLIENT_ID"),
        "client_secret": config("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config("REDIRECT_URI"),
    }

    return await http_client.SingletonAiohttp.query_url(
        config("DISCORD_API") + "/oauth2/token", method="POST", data=data, headers=headers
    )


async def get_user_from_discord(access_token: str):
    """
    Use the access token to fetch user's data from discord.
    """
    headers = {"Authorization": "Bearer {}".format(access_token)}
    return await http_client.SingletonAiohttp.query_url(config("DISCORD_API") + "/users/@me", headers=headers)


async def get_user_guilds_from_discord(access_token: str):
    """
    Use the access token to fetch user's guilds from discord.
    """
    headers = {"Authorization": "Bearer {}".format(access_token)}
    return await http_client.SingletonAiohttp.query_url(config("DISCORD_API") + "/users/@me/guilds", headers=headers)


async def get_bot_guilds_from_discord():
    headers = {"Authorization": f"Bot {config('BOT_TOKEN')}"}
    return await http_client.SingletonAiohttp.query_url(config("DISCORD_API") + "/users/@me/guilds", headers=headers)


async def match_guilds(user_guilds, bot_guilds) -> T.List:
    selected_guilds = []
    for g in user_guilds:
        if int(g["permissions"]) & 0x00000020:
            for b in bot_guilds:
                if g["id"] == b["id"]:
                    selected_guilds.append(g)

    return selected_guilds


@router.get("/@me")
async def get_user(code: str, checkPerms: bool = True):
    """
    Get the user's data & guilds from discord.
    """
    response = await exchange_code(code)

    try:
        access_token = response.get("access_token")
    except:
        print("Access Token Not Found!")
        return response

    user = await get_user_from_discord(access_token)
    user_guilds = await get_user_guilds_from_discord(access_token)
    bot_guilds = await get_bot_guilds_from_discord()

    user["guilds"] = await match_guilds(user_guilds, bot_guilds)

    return user


@router.get("/@db")
async def get_user_from_db(user_id: str):
    """
    Get the user's data from the database.
    """
    ...
