from configuration import config

DATABASE_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": config.POSTGRES_HOST.get_secret_value(),
                "port": config.POSTGRES_PORT.get_secret_value(),
                "user": config.POSTGRES_USER.get_secret_value(),
                "password": config.POSTGRES_PASSWORD.get_secret_value(),
                "database": config.POSTGRES_DB.get_secret_value(),
            }
        }
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    }
}