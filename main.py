from r_bot import bot, TOKEN



bot.run(TOKEN)

# from PIL import Image

# from civ5draft import Draft, DraftImage
#
# players = ["Ninjesus", "JBJBorn", 'Степан Яремба', 'R-Bot', 'NO_NAME', 'SNW']
# draft = Draft(players, num_nations=4)
# avs = [
#           Image.open("civ5draft/icons/avatars/av1.png"),
#           Image.open("civ5draft/icons/avatars/av2.png"),
#           Image.open("civ5draft/icons/avatars/av0.png"),
#           Image.open("civ5draft/icons/avatars/av3.png"),
#        ] + [None] * 2
# avatars = {players[i]: avs[i] for i in range(len(players))}
# draft_image = DraftImage(draft.drafted_nations, avatars=avatars)
# di = draft_image.get_image()
# # di.resize((di.width//4, di.height//4)).save("test.png")
# di.resize((di.width//4, di.height//4)).show()