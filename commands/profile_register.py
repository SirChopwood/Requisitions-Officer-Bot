import embedtemplates
import json
import discord

async def Main(self, message, command, arguments):
    test = self.database.get_user(message.guild.id, message.author.id)
    if test is not None:
        await message.channel.send(content="", embed=embedtemplates.failure("Already Registered",
                                                                            "You have already registered in this guild!"))
        return
    messages = []
    with open("json_files/user_profile.json", "r") as file:
        template = json.load(file)
    template["DiscordID"] = message.author.id

    messages.append(await message.channel.send(content="", embed=embedtemplates.question("What is your FIRST name? (Max 10 Characters)",
                                                                         message.author.display_name)))
    response = await self.await_response(message.author)
    if response is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    template["FirstName"] = response.content
    messages.append(response)

    messages.append(await message.channel.send(content="", embed=embedtemplates.question("What is your LAST name? (Max 10 Characters)",
                                                                                         message.author.display_name)))
    response = await self.await_response(message.author)
    if response is None:
        await message.channel.send(content="", embed=embedtemplates.failure("Response Timed Out",
                                                                            "You took too long to respond!"))
        return
    template["LastName"] = response.content
    messages.append(response)

    self.database.add_user(message.guild.id, template)
    settings = self.database.get_settings(message.guild.id)
    if settings["RegisterRole"] != 0:
        role = message.guild.get_role(settings["RegisterRole"])
        try:
            await message.author.add_roles(role)
        except discord.Forbidden:
            await message.channel.send(content="", embed=embedtemplates.failure("Missing Permissions",
                                                                                str(
                                                                                    "I do not have permissions to set your roles, " + message.author.display_name)))
            return

    await self.run_file("setname", message, arguments)
    await message.channel.send(content="", embed=embedtemplates.success("User Registered", str("Welcome " + message.author.mention)))
    embed = embedtemplates.profile(self, message.guild.id, message.author)
    await message.channel.send(content="", embed=embed)
    for m in messages:
        try:
            await m.delete()
        except discord.Forbidden:
            continue
