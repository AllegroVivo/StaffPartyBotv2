from __future__ import annotations

import os

from discord import Intents
from dotenv import load_dotenv

from Classes.Core.Bot import StaffPartyBot
################################################################################

load_dotenv()
DEBUG = os.getenv("DEBUG") == "True"

################################################################################

bot = StaffPartyBot(
    description="Staff Party Bus - Honk Honk!",
    intents=Intents.all(),
    debug_guilds=[
        955933227372122173,  # Bot Resources
        # 1104515062187708525,  # Staff Party Bus
        1273061765831458866,  # Kupo Nutz
    ] if DEBUG else None
)

################################################################################

for filename in os.listdir("Cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"Cogs.{filename[:-3]}")

################################################################################

token = os.getenv(("DEBUG" if DEBUG else "DISCORD") + "_TOKEN")
bot.run(token)

################################################################################
