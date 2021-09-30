import logging
from pathlib import Path

from dynaconf import Dynaconf, Validator

# LOGGING
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("core")
logger.setLevel(logging.INFO)


# CORE SETTINGS
settings = Dynaconf(
    dynaconf_merge=True,
    envvar_prefix=False,
    validators=[
        # DATABASE
        Validator(
            "DB_CONFIG.DB_HOST",
            "DB_CONFIG.DB_NAME",
            "DB_CONFIG.DB_USER",
            must_exist=True,
            is_type_of=str,
        ),
        Validator("DB_CONFIG.DB_PORT", must_exist=True, is_type_of=int),
        Validator("DB_CONFIG.DB_PASS", must_exist=True, is_type_of=str)
        | Validator("DB_CONFIG.DB_PASS", must_exist=True, is_type_of=int),
        Validator("DB_CONFIG.DB_ENGINE_CONSTANT", must_exist=True, is_type_of=str),
    ],
    environments=True,
    settings_files=[
        "settings.toml",
        ".secrets.toml",
    ],
)
