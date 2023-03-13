from decouple import config
import pytz

IST = pytz.timezone("Asia/Kolkata")

TORTOISE_CONF = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": config("PSQL_HOST"),
                "port": "5432",
                "user": config("PSQL_USER"),
                "password": config("PSQL_PASSWORD"),
                "database": config("PSQL_DATABASE"),
                "max_cached_statement_lifetime": 0,
                "max_cacheable_statement_size": 0,
            },
        }
    },
    "apps": {
        "models": {
            "models": ["src.models"],
            "default_connection": "default",
        },
    },
    "use_tz": True,
    "timezone": "Asia/Kolkata",
}
