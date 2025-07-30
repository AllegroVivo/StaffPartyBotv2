from __future__ import annotations

from typing import TYPE_CHECKING, List
from discord import Interaction, Embed, EmbedField
from discord.ext.pages import Page, PageGroup

from UI.Common import Frogginator

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("HelpMessage",)


################################################################################
class HelpMessage:
    __slots__ = (
        "_state",
    )

################################################################################
    def __init__(self, bot: StaffPartyBot):

        self._state: StaffPartyBot = bot

################################################################################
    async def menu(self, interaction: Interaction) -> None:

        page_groups = self._prepare_page_groups()
        frogginator = Frogginator(
            pages=page_groups,
            show_menu=True,
            menu_placeholder="Select your situation to get more info..."
        )
        await frogginator.respond(interaction)

################################################################################
    def _prepare_page_groups(self) -> List[PageGroup]:

        return [
            PageGroup(
                label="Start Here",
                pages=[
                    self._welcome_page()
                ]
            ),
            PageGroup(
                label="Interaction Failed",
                description="I got a failure while trying to interact with SPB.",
                pages=[
                    self.interaction_failed_page(),
                ]
            ),
            PageGroup(
                label="I Am a Venue Manager",
                description="I am a venue manager looking for staff.",
                pages=[
                    self.venue_manager_start(),
                    self.venue_manager_page1(),
                    self.venue_manager_page2(),
                    self.venue_manager_page3(),
                    self.venue_manager_page4(),
                    self.venue_manager_page5(),
                    self.venue_manager_page7(),
                    self.venue_manager_page6(),
                ]
            ),
            PageGroup(
                label="I am Staff",
                description="I am a staff member looking for work.",
                pages=[
                    self.staff_member_start(),
                    self.staff_member_page1(),
                    self.staff_member_page2(),
                    self.staff_member_page3(),
                    self.staff_member_page4(),
                    self.staff_member_page5(),
                    self.staff_member_page6(),
                ]
            ),
            PageGroup(
                label="I am a Trainee",
                description="I am new and looking for training.",
                pages=[
                    self.trainee_start(),
                    self.trainee_page1(),
                    self.trainee_page2(),
                    self.trainee_page3(),
                ]
            )
        ]

################################################################################
    @staticmethod
    def _welcome_page() -> Page:

        embed = Embed(
            title="__Welcome to the Staff Party Bus!__",
            description=(
                "The purpose of this server is to provide **fill-in staff** "
                "to venues who might experience a last minute shortage.\n\n"

                "It also offers staff and DJs a wide range of venue experience "
                "and resources:\n\n"

                "* **Internship** - __Learn new skills and improve existing ones.__\n"
                "*Venues can select candidates who are looking for training "
                "through an internship selection.*\n\n"

                "* **BG Check** - __All staff members are cleared.__\n"
                "*We require all experienced staff to complete a (short) "
                "background check before they can create their profile.*\n\n"

                "Select your situation from the menu below to get more information."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def interaction_failed_page() -> Page:
        embed = Embed(
            title="__I Got a Message Saying 'Interaction Failed'__",
            description=(
                "An interaction failed message means that the command you "
                "tried to use is most likely no longer available or has expired.\n\n"
                
                "Don't worry, this is normal! You can simply try re-invoking the "
                "command again and resume where you left off."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_start() -> Page:

        embed = Embed(
            title="__Help! I'm a Venue Manager and I Need Staff!__",
            description=(
                "The following pages contain information on the these topics:\n\n"

                "* **How to Create Your Venue Profile**\n"
                "* **What if Import Isn't Working?**\n"
                "* **Updating Profile Information**\n"
                "* **Adding a Manager to Your Venue**\n"
                "* **How to Post a Job Offer**\n"
                "* **Muting Job Offers for Selected Staff**\n\n"

                "Click the arrow buttons below to navigate through the pages."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page1() -> Page:

        embed = Embed(
            title="__How do I create my venue profile?__",
            description=(
                "Venue profile creation in Staff Party Bus is a simple process.\n"
                "Just follow these steps:\n\n"

                "1. **List your venue with FFXIV Venues**\n"
                "> Our venue profiles process partners with and relies heavily "
                "on FFXIV Venues. You'll need to create a venue there before "
                "you can make one with us. Check it out at "
                "https://discord.com/channels/1104515062187708525/1158618747356065902\n\n"

                "2. **Import your venue by creating your SPB venue profile.**\n"
                "> Once you've created your venue on FFXIV Venues, you can "
                "import it into Staff Party Bus with the </venue profile:1399882951453311113>. "
                "This will automatically populate your venue profile with the information you've "
                "already provided.\n\n"

                "3. **Review and update information**\n"
                "> After importing your venue, you'll need to review the "
                "information as well as update a few items unique to your venue "
                "with us. (There are buttons indicating what you can edit.)\n\n"

                "4. **Update from FFXIV Venues**\n"
                "> Once your profile is posted with SPB, and you make changes "
                "to your venue on FFXIV Venues, you can either use the "
                "**'Update from FFXIV'** button on your venue profile dashboard, "
                "otherwise your changes will update automatically within 24 hours."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page2() -> Page:

        embed = Embed(
            title="__I can't use </venue profile:1399882951453311113>! What do I do?__",
            description=(
                "If you're having trouble importing your venue, there are a "
                "few things you can try to fix the issue:\n\n"

                "1. **Check your venue on FFXIV Venues**\n"
                "> Make sure your venue is registered with FFXIV Venues and that "
                "you've been approved.\n\n"

                "2. **Check your permissions**\n"
                "> Make sure your discord user is associated with the venue "
                "on FFXIV Venues as a manager. If you cannot make administrative "
                "updates to your venue on their platform, you'll be unable to "
                "import/make updates in Staff Party Bus\n\n"

                "If none of these steps work, you can contact a server "
                "administrator for further assistance."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page3() -> Page:

        embed = Embed(
            title="__How do I update my venue's profile/information__",
            description=(
                "Updating your venue's profile is a simple process.\n"
                "Just follow these steps:\n\n"

                "1. **Update your profile on FFXIV Venues**\n"
                "> If you need to make changes to venue information such as "
                "schedule, address and/or management, you'll need to make those changes "
                "on your FFXIV Venues profile first. These changes will reflect on your "
                "SPB profile automatically within 24h -OR- you can use the "
                "**'Update From FFXIV'** button on your SPB profile dashboard to update "
                "venue listing immediately.\n\n"

                "2. **Use the </venue profile:1399882951453311113> command**\n"
                "> This command will display your venue profile dashboard. "
                "From here, you can make changes to your venue's other information "
                "such as the RP Level, hiring status, and staff application URL."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page4() -> Page:

        embed = Embed(
            title="__How do I add a manager to my venue?__",
            description=(
                "Adding a manager to your venue is pretty straightforward.\n\n"

                "**Update your profile on FFXIV Venues**\n"
                "> Managers are part of the information governed by "
                "FFXIV Venues, you'll need to request support on the FFXIV "
                "venue discord and ask them to make the modifications.  "
                "Then simply return here and run an update.\n\n"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page5() -> Page:

        embed = Embed(
            title="__How do I post a job offer?__",
            description=(
                "Posting a job offer is a simple process.\n\n"

                "1. **Access your venue profile by using </venue profile:1399882951453311113>**\n\n"

                "2. **Use the Temp/Perm Job management**\n"
                "> This button will open a menu where you can create, modify and delete "
                "job offers. You can include information such as the job type, "
                "description, and pay amount.\n\n"

                "3. **Post the job offer**\n"
                "> By completing the full process of creating a job offer, "
                "SPB will automatically post the job offer in the "
                "appropriate channel. This will also notify all eligible staff members"
                "who have opted in to receive job offers of the same type."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page6() -> Page:

        embed = Embed(
            title="__I don't want my job offers appearing for certain staff!__",
            description=(
                "Muting job offers for selected staff is as easy as a button "
                "click.\n\n"

                "1. **Navigate to the <#1224161402734772275> channel**\n"
                "> This channel contains all of our staff members' profiles. "
                "You can easily locate a given staff member by using the search "
                "function in the forum channel.\n\n"

                "2. **Click the '`Mute`' button on that staff member's profile**\n"
                "> This will prevent job offers from being sent to that staff "
                "member. They will still be able to see job offers in the job "
                "listings channel, but they will not receive a notification when "
                "a new job is posted."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def venue_manager_page7() -> Page:

        embed = Embed(
            title="__How do I edit/cancel my job posting?__",
            description=(
                "Editing or canceling a job posting is a simple process.\n\n"

                "1. **Access your venue profile by using </venue profile:1399882951453311113>**\n\n"
                
                "2. **Use the Temp/Perm Job management**\n"
                "> This button will open a menu where you can create, "
                "modify and delete job offers. \n"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_start() -> Page:

        embed = Embed(
            title="__I'm a Staff Member Looking for Work!__",
            description=(
                "The following pages contain information on these topics:\n\n"

                "* **How do I add Qualified Positions to my Staff Profile?**\n"
                "* **I'm having trouble posting my profile.**\n"
                "* **How do I get jobs?**\n"
                "* **Muting Job Offers from selected venues.**\n"
                "* **I have no RP work experience!**\n\n"

                "Click the arrow buttons below to navigate through the pages."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page1() -> Page:

        embed = Embed(
            title="__How do I add Qualified Positions to my Staff Profile?__",
            description=(
                "Adding Qualified Positions to your staff profile with SPB requires "
                "you to complete a *VERY* short background check outlining your "
                "work experience.\n\n"

                "1. **Use the </staff profile:1399882951453311109> command**\n"
                "> This command will open your profile menu. You must navigate to  "
                "the Main Info & Details subsection and select the Qualified Positions "
                "button. This will prompt a background check.\n\n"

                "2. **Wait...**\n"
                "> Once you've completed the background check, you'll need to wait "
                "for a server administrator to review your information. This "
                "usually takes only a few minutes.\n\n"

                "3 **You'll get a DM when you're approved!**\n"
                "> Once you're approved, you'll receive a DM from the Staff Party Bus "
                "indicating that you can complete your staff profile.\n\n"

                "**Remember, the goal of Staff Party Bus is to provide reliable and "
                "professional staff to venues in need, and the BG check is a part of "
                "that process.**"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page2() -> Page:

        embed = Embed(
            title="__How do I create my staff profile?__",
            description=(
                "Creating your staff profile is a simple process.\n\n"

                "1. **Use the </staff profile:1399882951453311109> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the staff profile creation process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"

                "2. **Ensure you complete all the required information!**\n"
                "> The staff profile creation process requires you to provide some "
                "basic information about yourself, including your **home region(s)**, "
                "**work availability**, **employable positions**, and **character name.**\n\n"

                "__**Hey, my image isn't uploading!**__\n"
                "> If you're having trouble uploading your image, make sure it's of "
                "the correct format. We only accept **WEBP**, **GIF**, **PNG** "
                "and **JPEG** files. \n\n"
                
                "If you're still having trouble, contact a server administrator!"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page3() -> Page:

        embed = Embed(
            title="__It won't let me post my profile!__",
            description=(
                "Not a problem, just ensure you've completed all the required sections.\n\n"

                "**Ensure you complete all the required information!**\n"
                "> The staff profile creation process requires you to provide some "
                "basic information about yourself:\n"
                "> * **Character Name**\n"
                "> * **Qualified Positions**\n"
                "> * **Home Region(s)**\n"
                "> * **RP Preference**\n"
                "> * **Preferred Tags**\n"
                "> * **Timezone**\n"
                "> * **Availability**\n\n"
                
                "If you're still having trouble, contact a server administrator."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page4() -> Page:

        embed = Embed(
            title="__How do I get jobs?__",
            description=(
                "Getting jobs in Staff Party Bus is a simple process.\n\n"

                "The Staff Party Bus will automatically send you a DM when a "
                "job offer is posted that matches your profile. You can also view "
                "job offers in the job listings channel.\n\n"

                "(If you're not receiving DMs, you can check your profile to ensure "
                "you've set your availability and employable positions correctly.)\n\n"

                "You can also view job offers in the job listings channels.\n\n"
                
                "https://discord.com/channels/1104515062187708525/1224185349924978808\n"
                "-and-\n"
                "https://canary.discord.com/channels/1104515062187708525/1397729522299699242\n\n"
                
                "If you see a job offer you like, you can apply for it by clicking the "
                "button on the job offer message.\n\n"

                "__**I don't want to receive DMs anymore.**__\n"
                "> If you no longer want to receive DMs when job offers are posted, "
                "you can change your Qualified Positions to **None** in your Staff profile. "
                "This will prevent SPB from sending you DMs until you reactivate your profile."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page5() -> Page:

        embed = Embed(
            title="__I don't want to receive DMs from certain venue(s)__",
            description=(
                "Muting job offers from selected venues is as easy as a button click.\n\n"

                "1. **Navigate to the <#1222976936360415303> channel**\n"
                "> This channel contains all of our venue profiles. You can easily "
                "locate a given venue by using the search function in the forum channel.\n\n"

                "2. **Click the '`Mute`' button on that venue's profile**\n"
                "> This will prevent job offers from that venue from being sent to you. "
                "You will still be able to see job offers in the job listings channel, "
                "but you will not receive a notification when a new job is posted."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def staff_member_page6() -> Page:

        embed = Embed(
            title="__I have no work experience, but still want jobs!__",
            description=(

                "1. **Use the </staff profile:1399882951453311109> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the staff profile creation process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"

                "2. Fill out all the information in Main Info & Details. Fill out "
                "the Desired Trainings you want to receive.\n\n"

                "3. When a venue selects you for an Internship, SPB will send you a DM "
                "and a private channel will be created to communicate with the venue management.\n\n"

                "4. An Internship is just a training via a venue. This doesn't obligate you to "
                "work for them.\n\n"

                "For more information, see the relevant section in this help message!"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_start() -> Page:

        embed = Embed(
            title="__I have no experience in venue employment!__",
            description=(
                "The following pages contain information on these topics:\n\n"

                "* **How do I get training?**\n"
                "* **How do I know if a venue has picked me?**\n"
                "* **What exactly does 'internship' entail?**\n"

                "Click the arrow buttons below to navigate through the pages."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_page1() -> Page:

        embed = Embed(
            title="__How do I get training?__",
            description=(
                "Getting started with training in Staff Party Bus is a simple process.\n\n"

                "1. **Use the </staff profile:1399882951453311109> command**\n"
                "> This command will display a message with some buttons allowing "
                "you to complete the staff profile creation process. This is a simple "
                "process that requires only a few clicks and answers.\n\n"

                "2. **Ensure you complete all the required information!**\n"
                "> The staff profile creation process requires you to provide some "
                "basic information about yourself:\n"
                "> * **Character Name**\n"
                "> * **Home Region(s)**\n"
                "> * **Desired Training**\n"
                "> * **RP Preference**\n"
                "> * **Preferred Tags**\n"
                "> * **Timezone**\n"
                "> * **Availability**\n"

                "3. **Prepare for training!**\n"
                "> Once you've completed your profile, you can prepare for training. "
                "This includes reading the venue </etiquette:1399888918845067327> guide "
                "and reading on the general position description by using the "
                "https://discord.com/channels/1104515062187708525/1399747104947175556 channel.\n\n"

                "4. **Wait for a venue to pick you up!**\n"
                "> SPB will send you a DM once a venue has selected you for an internship. "
                "A private channel will be created to communicate with venue management."
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_page2() -> Page:

        embed = Embed(
            title="__How do I know if a venue has picked me?__",
            description=(
                "You'll receive a DM from the Staff Party Bus when a venue "
                "has selected you for internship. A private channel will be created "
                "to communicate with the venue management.\n"
            )
        )

        return Page(embeds=[embed])

################################################################################
    @staticmethod
    def trainee_page3() -> Page:

        embed = Embed(
            title="__What exactly does 'internships' entail?__",
            description=(
                "Internships is a simple process that involves getting "
                "in-venue training to learn the ropes of a given position.\n\n"

                "1. **Read the venue etiquette guide**\n"
                "> Before your internships, you should read the venue "
                "</etiquette:1399882951453311112> guide. This will give you an idea of "
                "what to expect from the venue community.\n\n"

                "2. **Talk with management**\n"
                "> After selecting you, A private channel will be created "
                "to communicate with the venue management. This primarily involves "
                "setting an appropriate time for the training.\n\n"

                "3. **Work with management**\n"
                "> During your internship, you'll learn the ropes of the position. "
                "This may involve shadowing them during a shift "
                "or working alongside them to complete tasks.\n\n"

                "4. **Complete your internship**\n"
                "> Once you feel you are qualified for this position,  "
                "you can update the Qualified Positions in your </staff profile:1399882951453311109>. "
            )
        )

        return Page(embeds=[embed])

################################################################################
