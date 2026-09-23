import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("DJANGO_ENV", "dev").lower()

if env == "dev":
    from .dev import *
if env == "prod":
    from .prod import *