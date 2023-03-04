from fastapi import APIRouter

from utils import http_client
from decouple import config

router = APIRouter()


async def get_guild_from_discord(guild_id: str):
    """
    Fetch guild's data from discord.
    """
    headers = {"Authorization": f'Bot {config("BOT_TOKEN")}'}

    url = config("DISCORD_API") + f"/guilds/{guild_id}"

    return await http_client.SingletonAiohttp.query_url(url, headers=headers)


async def get_guild_channels(guild_id: str):
    headers = {"Authorization": f'Bot {config("BOT_TOKEN")}'}
    url = config("DISCORD_API") + f"/guilds/{guild_id}/channels"

    return await http_client.SingletonAiohttp.query_url(url, headers=headers)


@router.get("/")
async def get_guild(id: str, useCache: bool = True):
    """
    Returns guild's info from discord / cache
    """
    guild = await get_guild_from_discord(id)
    channels = await get_guild_channels(id)

    guild["channels"] = channels

    return guild
