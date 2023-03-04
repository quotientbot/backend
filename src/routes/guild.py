from fastapi import APIRouter
import aiohttp
from decouple import config

router = APIRouter()


async def get_guild_from_discord(guild_id: str):
    """
    Fetch guild's data from discord.
    """
    headers = {"Authorization": f'Bot {config("BOT_TOKEN")}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        url = config("DISCORD_API") + f"/guilds/{guild_id}"
        async with session.get(url) as response:
            data = await response.json()
            return data


async def get_guild_channels(guild_id: str):
    headers = {"Authorization": f'Bot {config("BOT_TOKEN")}'}

    async with aiohttp.ClientSession(headers=headers) as session:
        url = config("DISCORD_API") + f"/guilds/{guild_id}/channels"
        async with session.get(url) as response:
            data = await response.json()
            return data


@router.get("/")
async def get_guild(id: str, useCache: bool = True):
    """
    Returns guild's info from discord / cache
    """

    guild = await get_guild_from_discord(id)
    channels = await get_guild_channels(id)

    guild["channels"] = channels
    return guild
