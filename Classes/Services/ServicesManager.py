from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from discord import Interaction, User, Embed, ButtonStyle, SelectOption, EmbedField
from discord.ext.pages import Page

from Classes.Common import ObjectManager, RevisitTimer
from Enums import Service, XIVRegion
from UI.Common import FroggeView, FroggeSelectView, ConfirmCancelView, BasicTextModal, Frogginator
from UI.Services import NoServicesAddView
from Utilities import Utilities as U
from .ServiceRequest import ServiceRequest


if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("ServicesManager", )

################################################################################
class ServicesManager(ObjectManager):

    __slots__ = (
        "_revisits",
    )

################################################################################
    def __init__(self, bot: StaffPartyBot) -> None:

        super().__init__(bot)

        self._revisits: List[RevisitTimer] = []

################################################################################
    async def load_all(self, payload: Any) -> None:

        self._managed = [
            ServiceRequest(self, **data)
            for data
            in payload.get("service_requests", [])
        ]

################################################################################
    async def finalize_load(self) -> None:

        for request in self._managed:
            await request.refresh()
            await request.update_post_components()

        print("Finalized loading of service requests.")

################################################################################
    @property
    def service_requests(self) -> List[ServiceRequest]:

        return self._managed

################################################################################
    async def status(self) -> Embed:

        pass

################################################################################
    def get_menu_view(self, user: User) -> FroggeView:

        pass

################################################################################
    async def add_item(self, interaction: Interaction) -> None:

        pass

################################################################################
    async def modify_item(self, interaction: Interaction) -> None:

        pass

################################################################################
    async def remove_item(self, interaction: Interaction) -> None:

        pass

################################################################################
    async def request_wizard(self, interaction: Interaction) -> None:

        # Service Category
        prompt = U.make_embed(
            title="Request for Service: Service Type",
            description=(
                "Please select the type of service you would like to make "
                "a request for.\n\n"
                
                "This prompt is __**mandatory**__ to ensure that the request "
                "is properly categorized and directed appropriately."
            ),
        )
        view = FroggeSelectView(interaction.user, options=Service.select_options(), show_close=False)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete or view.value is False:
            return

        service = Service(int(view.value))

        # Description
        prompt = U.make_embed(
            title="Request for Service: Description",
            description=(
                "Would you like to provide a brief description of the service you are "
                "requesting?\n\n"
                
                "*This prompt is __**optional**__ but highly recommended "
                "to ensure that the request is properly understood and addressed.*"
            ),
        )
        view = ConfirmCancelView(interaction.user, return_interaction=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return

        if view.value is False:
            description = None
        else:
            _, inter = view.value
            modal = BasicTextModal(
                title="Service Description",
                attribute="Description",
                example="eg. 'I would like to redesign my venue's logo.'",
                max_length=500,
                multiline=True
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            description = modal.value

        # Budget
        prompt = U.make_embed(
            title="Request for Service: Budget",
            description=(
                "Would you like to provide a budget for the service you are requesting?\n\n"
                
                "*This prompt is __**optional**__ but highly recommended "
                "to ensure that the request is properly understood and addressed.*"
            ),
        )
        view = ConfirmCancelView(interaction.user, return_interaction=True)

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return
        elif view.value is False:
            budget = None
        else:
            _, inter = view.value
            modal = BasicTextModal(
                title="Service Budget",
                attribute="Budget",
                example="eg. '10.5m or 10,500,000''",
                max_length=100,
            )

            await inter.response.send_modal(modal)
            await modal.wait()

            if not modal.complete:
                return

            budget = modal.value

        # Data Center
        prompt = U.make_embed(
            title="Request for Service: Home Region",
            description=(
                "Please select the home region in which the services will "
                "be rendered.\n\n"

                "*This prompt is __**optional**__ as not all services are "
                "region-specific.*"
            ),
        )
        view = ConfirmCancelView(
            owner=interaction.user,
            return_interaction=True,
            confirm_text="Select Region",
            cancel_text="Not Applicable",
            cancel_style=ButtonStyle.primary,
        )

        await interaction.respond(embed=prompt, view=view)
        await view.wait()

        if not view.complete:
            return
        elif view.value is False:
            data_center = None
        else:
            options = XIVRegion.select_options()
            options.append(SelectOption(label="Not Applicable", value="-1"))

            prompt = U.make_embed(
                title="Select Your Data Center",
                description=(
                    "Please select the region in which the services will be rendered."
                ),
            )
            view = FroggeSelectView(interaction.user, options=options, show_close=False)

            await interaction.respond(embed=prompt, view=view)
            await view.wait()

            if not view.complete:
                return

            if view.value == "-1":
                data_center = None
            else:
                data_center = XIVRegion(int(view.value))

        request = ServiceRequest.new(
            mgr=self,
            user=interaction.user,
            service=service,
            description=description,
            budget=budget,
            dc=data_center
        )
        self._managed.append(request)

        await request.confirmation_menu(interaction)

################################################################################
    async def user_menu(self, interaction: Interaction) -> None:

        frogginator = Frogginator(await self.make_pages(interaction.user.id), self, default_button_row=3)
        await frogginator.respond(interaction)

################################################################################
    async def make_pages(self, user_id: int) -> List[Page]:

        user_requests = [
            req
            for req in self.service_requests
            if req.user_id == user_id
        ]
        pages = [await req.page() for req in user_requests]
        if not pages:
            pages.append(
                Page(
                    embeds=[
                        U.make_embed(
                            title="No Service Requests",
                            description=(
                                "You have no service requests at this time.\n"
                                "Please use the button below to create one!"
                            )
                        )
                    ],
                    custom_view=NoServicesAddView()
                )
            )

        return pages

################################################################################
    async def check_revisits(self):

        final = []

        for revisit in self._revisits:
            if revisit.is_expired():
                await revisit.context.revisit()
            else:
                final.append(revisit)

        self._revisits = final

################################################################################
    def register_revisit(self, request: ServiceRequest, duration_sec: int = 30) -> None:  # 3 days 259200

        self._revisits.append(RevisitTimer(request, duration_sec))

################################################################################
