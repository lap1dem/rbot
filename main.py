from PIL import Image

from src.civ5draft import Draft, DraftImage
from src.civ5draft.image_utils import concat_images

players = ["Ninjesus", "JBJBorn", 'Степан Яремба', 'R-Bot', 'NO_NAME', 'SNW']
draft = Draft(players)
avs = [
          Image.open("src/civ5draft/icons/avatars/av1.png"),
          Image.open("src/civ5draft/icons/avatars/av2.png"),
          Image.open("src/civ5draft/icons/avatars/av0.png"),
          Image.open("src/civ5draft/icons/avatars/av3.png"),
       ] + [None] * 2
avatars = {players[i]: avs[i] for i in range(len(players))}
draft_image = DraftImage(draft.drafted_nations, avatars=avatars)
di = draft_image.get_image()
di.resize((di.width//2, di.height//2)).save("test.png")