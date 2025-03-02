from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Dict, Type, TypeVar

from discord import EmbedField, Embed
from discord.ext.pages import Page

from Classes.Common import Identifiable
from UI.Profiles import AdditionalImageEditView
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import ProfileImages, StaffPartyBot
################################################################################

__all__ = ("AdditionalImage", )

AI = TypeVar("AI", bound="AdditionalImage")

################################################################################
class AdditionalImage(Identifiable):

    __slots__ = (
        "_parent",
        "_url",
        "_caption",
    )

################################################################################
    def __init__(self, parent: ProfileImages, id: int, **kwargs) -> None:

        super().__init__(id)

        self._parent: ProfileImages = parent

        self._url: str = kwargs["url"]
        self._caption: Optional[str] = kwargs.get("caption")

################################################################################
    @classmethod
    def new(cls: Type[AI], parent: ProfileImages, url: str, caption: Optional[str]) -> AI:

        new_data = parent.bot.db.insert.additional_image(parent.profile_id, url, caption)
        return cls(parent, **new_data)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    @property
    def url(self) -> str:

        return self._url

################################################################################
    @property
    def caption(self) -> Optional[str]:

        return self._caption

################################################################################
    def delete(self) -> None:

        self.bot.db.delete.additional_image(self.id)
        self._parent._additional.remove(self)

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            title="__Additional Image Info__",
            description="(This image can be seen below.)",
            fields=[
                EmbedField(
                    name="__Permalink__",
                    value=self.url,
                    inline=False
                ),
                EmbedField(
                    name="__Caption__",
                    value=self.caption if self.caption is not None else "`Not Set`",
                    inline=False
                )
            ],
            image_url=self.url
        )

################################################################################
    def compile(self) -> str:

        if self.caption is None:
            return self.url

        return f"[{self.caption}]({self.url})"

################################################################################
    def page(self) -> Page:

        return Page(embeds=[self.status()], custom_view=AdditionalImageEditView(self))

################################################################################
