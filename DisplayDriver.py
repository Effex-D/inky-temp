import inkyphat
from PIL import ImageFont
from random import randint

class DisplayDriver():

    def __init__(self):
        # Do I need to initialize something?
        something = "Nothing"

    def display_notification_message(self, data):

        message = data[0]
        message2 = data[1]
        message3 = data[2]

        inkyphat.set_colour("black")

        font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 26)
        font2 = ImageFont.truetype(inkyphat.fonts.FredokaOne, 20)
        font3 = ImageFont.truetype(inkyphat.fonts.FredokaOne, 14)

        print(message)
        print(message2)
        print(message3)

        w, h = font.getsize(message)
        x = (inkyphat.WIDTH / 2) - (w / 2)
        y = (inkyphat.HEIGHT / 3) - (h / 1.5)
        inkyphat.text((x, y), message, inkyphat.BLACK, font)

        w, h = font2.getsize(message2)
        x = (inkyphat.WIDTH / 2) - (w / 2)
        y = (inkyphat.HEIGHT / 2) - 5
        inkyphat.text((x, y), message2, inkyphat.BLACK, font2)

        w, h = font2.getsize(message3)
        x = (inkyphat.WIDTH / 2) - (w / 2)
        y = (inkyphat.HEIGHT / 3) * 2
        inkyphat.text((x, y), message3, inkyphat.BLACK, font2)

        inkyphat.show()