from fastapi import APIRouter
import aiohttp
from decouple import config

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

    async with aiohttp.ClientSession() as session:
        async with session.post(
            config("DISCORD_API") + "/oauth2/token", data=data, headers=headers
        ) as res:
            return await res.json()


async def get_user_from_discord(access_token: str):
    """
    Use the access token to fetch user's data from discord.
    """
    headers = {"Authorization": "Bearer {}".format(access_token)}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            config("DISCORD_API") + "/users/@me", headers=headers
        ) as response:
            return await response.json()


async def get_user_guilds_from_discord(access_token: str):
    """
    Use the access token to fetch user's guilds from discord.
    """
    headers = {"Authorization": "Bearer {}".format(access_token)}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            config("DISCORD_API") + "/users/@me/guilds", headers=headers
        ) as response:
            return await response.json()


@router.get("/@me")
async def get_user(code: str):
    """
    Get the user's data & guilds from discord.
    """
    response = await exchange_code(code)
    access_token = response.get("access_token")
    if not access_token:
        print("Access Token Not Found!")
        return response

    user = await get_user_from_discord(access_token)
    guilds = await get_user_guilds_from_discord(access_token)
    user["guilds"] = guilds
    return user
