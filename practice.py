from PIL import Image,ImageFont,ImageDraw

my_image=Image.open("black.png")

title_font = ImageFont.truetype('playfair/playfair-font.ttf', 200)
print(title_font)

#title_text = "The Beauty of Nature"

#image_editable = ImageDraw.Draw(my_image)

#image_editable.text((15,15), title_text, (237, 230, 211), font=title_font)

#my_image.save("result.jpg")