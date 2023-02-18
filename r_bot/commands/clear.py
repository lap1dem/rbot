import discord as dc
from ..bot import bot


@bot.slash_command(
    name="clear",
    description="Clear channel from threads and messages.",
)
async def clear(ctx: dc.ApplicationContext):
    reaction = await ctx.respond("⏳ Wait a second...")
    channel = ctx.channel
    for thread_ in channel.threads:
        await thread_.delete()
    messages = await channel.history(limit=100).flatten()
    await channel.delete_messages(messages)
