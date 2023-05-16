from ..bot import bot


@bot.event
async def on_raw_reaction_add(payload):
    if "980644696571400324" in str(payload.emoji):
        guild = bot.get_guild(payload.guild_id)
        channel = await bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        for reaction in message.reactions:
            if reaction.emoji.id == 980644696571400324 and reaction.count < 2:
                await message.remove_reaction(payload.emoji, payload.member)
                await message.add_reaction("<a:pepe_honkler:985937888925585408>")
                break
