from __future__ import annotations

from typing import Literal

from discord.abc import GuildChannel

from Utilities.ErrorMessage import ErrorMessage
################################################################################

__all__ = ("InvalidChannelType",)

################################################################################
class InvalidChannelType(ErrorMessage):

    def __init__(self, channel: GuildChannel, expected_type: Literal["Text", "Voice", "Forum"]):

        super().__init__(
            title="Invalid Channel Type",
            message=f"The channel {channel.mention} is not of type `{expected_type} Channel`.",
            solution=f"Please ensure you mention a valid {expected_type} Channel."
        )

################################################################################
