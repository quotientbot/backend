from fastapi import FastAPI, Depends, HTTPException
from decouple import config
from fastapi.security import APIKeyHeader
from routes import auth, user
from fastapi.middleware.cors import CORSMiddleware

api_scheme = APIKeyHeader(name="authorization")


async def verify_key(key: str = Depends(api_scheme)):
    if key != config("API_KEY"):
        raise HTTPException(status_code=403)


app = FastAPI(debug=True)

# dependencies=[Depends(verify_key)]
app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")


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
