from PIL import Image
import matplotlib.pyplot as plt
verified_dark=Image.open("verified_dark.png")
verified_dark=verified_dark.convert("RGB")
 
d = verified_dark.getdata()
#print(len(d))


new_image = []

for item in d:
	#print(item)
	if item[0] in list(range(200,256)):
		new_image.append((0,0,0))
	else:
		new_image.append((255,255,255))
		pass
	
verified_dark.putdata(new_image)
verified_dark.save("verified_dark.png")
plt.imshow(verified_dark)
verified_dark=verified_dark.convert("RGBA")
plt.show()