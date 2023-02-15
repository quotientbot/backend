from fastapi import APIRouter, responses
from decouple import config

router = APIRouter()


@router.get("/login")
async def login():
    return responses.RedirectResponse(config("DISCORD_REDIRECT"))
    
    
