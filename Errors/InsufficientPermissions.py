from __future__ import annotations

from discord.abc import GuildChannel

from Utilities.ErrorMessage import ErrorMessage
################################################################################

__all__ = ("InsufficientPermissions",)

################################################################################
class InsufficientPermissions(ErrorMessage):

    def __init__(self, channel: GuildChannel, permissions_needed: str):
    
        super().__init__(
            title="Insufficient Permissions",
            message=(
                f"You do not have the required permission(s) `{permissions_needed}` "
                f"to perform that action in the channel {channel.mention}."
            ),
            solution="Please contact a server administrator for assistance."
        )

################################################################################
