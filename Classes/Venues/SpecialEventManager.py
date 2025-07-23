from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from discord import Interaction, Embed, EmbedField, ForumChannel

from Errors import MaxItemsReached
from UI.Common import BasicTextModal, ConfirmCancelView, FroggeSelectView, ConfirmCancelView2
from UI.Venues import SpecialEventManagerMenuView
from .SpecialEvent import SpecialEvent
from Utilities import Utilities as U

if TYPE_CHECKING:
    from Classes import Venue, StaffPartyBot
################################################################################

__all__ = ("SpecialEventManager", )

################################################################################
class SpecialEventManager:

    __slots__ = (
        "_parent",
        "_events",
    )

    MAX_EVENTS = 20

################################################################################
    def __init__(self, parent: Venue, **kwargs) -> None:

        self._parent: Venue = parent
        self._events: List[SpecialEvent] = [
            SpecialEvent(self, **ev)
            for ev
            in kwargs.get("special_events", [])
        ]

################################################################################
    def __getitem__(self, event_id: int) -> SpecialEvent:

        return next((e for e in self._events if e.id == int(event_id)), None)

################################################################################
    @property
    def bot(self) -> StaffPartyBot:

        return self._parent.bot

################################################################################
    @property
    def venue(self) -> Venue:

        return self._parent

################################################################################
    @property
    def event_participation(self) -> bool:

        return self.venue.event_participation

    @event_participation.setter
    def event_participation(self, value: bool) -> None:

        self.venue.event_participation = value

################################################################################
    @property
    async def post_channel(self) -> Optional[ForumChannel]:

        return await self.bot.channel_manager.special_events_channel

################################################################################
    def status(self) -> Embed:

        return U.make_embed(
            title="Special Events Management",
            description=(
                "Click the toggle button below to enable or disable the bot from "
                "sending you notifications about special event participation "
                "requests.\n\n"
                
                "Otherwise, you can use the other buttons below to manage your "
                "venue's special events."
            ),
            fields=[EmbedField(
                name="__Event Participation Notifications__",
                value=U.yes_no_emoji(self.event_participation),
                inline=True
            )] + [e.summary_field() for e in self._events]
        )

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        embed = self.status()
        view = SpecialEventManagerMenuView(interaction.user, self)

        await interaction.respond(embed=embed, view=view)
        await view.wait()

################################################################################
    async def toggle_participation(self, interaction: Interaction) -> None:

        self.event_participation = not self.event_participation
        await interaction.edit()

################################################################################
    async def add_event(self, interaction: Interaction) -> None:

        if len(self._events) >= self.MAX_EVENTS:
            error = MaxItemsReached("Special Events", self.MAX_EVENTS)
            await interaction.respond(embed=error)
            return

        warning = U.make_embed(
            title="Event Creation Warning",
            description=(
                "**PLEASE NOTE:\n"
                "DMs will only be sent to potential participants ONE TIME for "
                "each event - at the time of creation.**\n\n"
                
                "*Any additional modifications made to the event after this "
                "process will be updated on your post in the special events "
                "channel, but will not result in any kind of DM-ping to "
                "participants.*\n\n"
            )
        )
        view = ConfirmCancelView(interaction.user, show_cancel=False, return_interaction=True)

        await interaction.respond(embed=warning, view=view)
        await view.wait()

        if not view.complete:
            return

        _, inter = view.value

        # Title
        modal = BasicTextModal(
            title="Enter Your Event Title",
            attribute="Title",
            example="e.g. 'The Great Hunt'"
        )

        await inter.response.send_modal(modal)
        await modal.wait()

        if not modal.complete:
            return

        title = modal.value
        description = location = start = length = links = requirements = None

        # Description
        prompt = U.make_embed(
            title="Event Description",
            description=(
                "Would you like to enter a description for your event?\n\n"
                
                "This is different from the event title and participant requirements."
                "It should be a short summary of the event.\n\n"
                
                "You can also skip this step and add a description later."
            )
        )
        view = ConfirmCancelView2(
            owner=interaction.user,
            confirm_text="Enter Description",
            cancel_text="Skip Description for Now",
            return_interaction=True
        )

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        result, inter = view.value
        if result is True:
            modal = BasicTextModal(
                title="Enter Your Event Description",
                attribute="Description",
                example="e.g. 'Join us for a grand hunt!'",
                max_length=500,
                multiline=True,
                return_interaction=True
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            description, inter = modal.value

        # Location
        prompt = U.make_embed(
            title="Event Location",
            description=(
                "Would you like to enter a location for your event?\n\n"
                
                "You can also skip this step and add a location later."
            )
        )
        view = ConfirmCancelView2(
            owner=interaction.user,
            confirm_text="Enter Location",
            cancel_text="Skip Location for Now",
            return_interaction=True
        )

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        result, inter = view.value
        if result is True:
            modal = BasicTextModal(
                title="Enter Your Event Location",
                attribute="Location",
                example="e.g. 'Central Park'",
                max_length=150,
                return_interaction=True
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            location, inter = modal.value

        # Start
        prompt = U.make_embed(
            title="Event Start Time",
            description=(
                "Would you like to enter the start time for your event now?\n\n"
                
                "You can also skip this step and add a start time later."
            )
        )
        view = ConfirmCancelView2(
            owner=interaction.user,
            confirm_text="Enter Start Time",
            cancel_text="Skip Start Time for Now",
            return_interaction=True
        )

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        result, inter = view.value
        if result is True:
            modal = BasicTextModal(
                title="Enter Your Event Start Time",
                attribute="Start Time",
                example="e.g. '2025-10-01 14:00 EST'",
                return_interaction=True
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            start, inter = modal.value

        # Length
        prompt = U.make_embed(
            title="Event Length",
            description=(
                "Would you like to enter the length of your event now?\n\n"
                
                "You can also skip this step and add a length later."
            )
        )
        view = ConfirmCancelView2(
            owner=interaction.user,
            confirm_text="Enter Length",
            cancel_text="Skip Length for Now",
            return_interaction=True
        )

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        result, inter = view.value
        if result is True:
            modal = BasicTextModal(
                title="Enter Your Event Length",
                attribute="Length",
                example="e.g. '120 hours'",
                return_interaction=True
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            length, inter = modal.value

        # Links
        prompt = U.make_embed(
            title="Event Links",
            description=(
                "Would you like to enter any links for your event now?\n\n"
                
                "You can also skip this step and add links later."
            )
        )
        view = ConfirmCancelView2(
            owner=interaction.user,
            confirm_text="Enter Links",
            cancel_text="Skip Links for Now",
            return_interaction=True
        )

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        result, inter = view.value
        if result is True:
            modal = BasicTextModal(
                title="Enter Your Event Links",
                attribute="Comma-Separated Links",
                example="e.g. 'https://example.com, https://example2.com'",
                max_length=1000,
                multiline=True,
                return_interaction=True
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            raw_links, inter = modal.value
            links = [link.strip() for link in raw_links.split(",")]

        # Requirements
        prompt = U.make_embed(
            title="Event Requirements",
            description=(
                "Would you like to enter any requirements for your event now?\n\n"
                
                "This is a list of requirements that participants must meet in order to "
                "participate in the event.\n\n"
                
                "**This should answer the question: 'What do I need to do to be able to "
                "participate in this event?'**\n\n"
                
                "You can also skip this step and add requirements later."
            )
        )
        view = ConfirmCancelView2(
            owner=interaction.user,
            confirm_text="Enter Requirements",
            cancel_text="Skip Requirements for Now",
            return_interaction=True
        )

        await inter.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        result, inter = view.value
        if result is True:
            modal = BasicTextModal(
                title="Enter Your Event Requirements",
                attribute="Requirements",
                example="e.g. 'Must be a member of the venue'",
                max_length=1000,
                multiline=True,
                return_interaction=True
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            requirements, inter = modal.value

        new_event = SpecialEvent.new(
            self,
            title=title,
            description=description,
            location=location,
            start=start,
            length=length,
            links=links,
            requirements=requirements
        )
        self._events.append(new_event)

        await new_event.post(inter)
        await inter.respond(
            f"**Event '{title}' has been created!**\n\n"
            
            f"**Title:** `{title}`\n"
            f"**Description:** {description}\n"
            f"**Location:** `{location}`\n"
            f"**Start Time:** `{start}`\n"
            f"**Length:** `{length}`\n"
            f"**Links:** {', '.join(links)}\n"
            f"**Requirements:** {requirements}\n\n"
            
            f"[Click here to see the posting!]({new_event.post_url})",
            ephemeral=True
        )

        await self.notify_venues_of_event(new_event)

################################################################################
    async def modify_event(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Event Modification",
            description="Please select the event you would like to modify."
        )
        options = [e.select_option() for e in self._events]
        view = FroggeSelectView(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        event = self[view.value]
        await event.menu(interaction)

################################################################################
    async def remove_event(self, interaction: Interaction) -> None:

        prompt = U.make_embed(
            title="Event Modification",
            description="Please select the event you would like to modify."
        )
        options = [e.select_option() for e in self._events]
        view = FroggeSelectView(interaction.user, options)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        event = self[view.value]
        await event.remove(interaction)

################################################################################
    async def notify_venues_of_event(self, event: SpecialEvent) -> None:

        venues = [
            v
            for v in self.bot.venue_manager.venues
            if v.event_participation
        ]
        for venue in venues:
            await venue.notify_of_event(event)

################################################################################
