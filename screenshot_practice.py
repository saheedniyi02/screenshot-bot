from PIL import Image,ImageFont,ImageDraw
import matplotlib.pyplot as plt
from pilmoji import Pilmoji
import numpy as np
import string
import emoji

test=Image.open("test1.jpg")


profile_pics = Image.open("effiong.jpg") 

#create mask
h,w = profile_pics.size 

  
# creating luminous image 

lum_img = Image.new('L',[h,w] ,0)  

draw = ImageDraw.Draw(lum_img) 

draw.pieslice([(0,0),(h,w)],0,360,fill=255) 

img_arr = np.array(profile_pics) 

lum_img_arr = np.array(lum_img) 
#display(Image.fromarray(lum_img_arr))
mask_im=Image.fromarray(lum_img_arr)


mask_im=mask_im.resize((130,130))
profile_pics=profile_pics.resize((130,130))

verified=Image.open("verified.png")
verified=verified.convert("RGB")
verified=verified.resize((40,40))

verified_dark=Image.open("verified_dark.png")
verified_dark=verified_dark.convert("RGB")
verified_dark=verified_dark.resize((60,60))


text="So I recently spoke with some entry level data peeps and I was surprised that only 1 in 10 had a portfolio. Tomorrow I will posting a video on how you can create a data science portfolio for free. I'm hoping you'd get a thing or two from it👍. #DataAnalytics #dataportfolio "


def check_last_space(last_index,text):
    while last_index>1:
        if text[last_index]!=" ":
            last_index=last_index-1
        else:
            return text[:last_index],last_index
            
            
def clean_text(text):
  words_per_line=32
  no_lines=(len(text)//words_per_line)+1
  lines=[]
  for line_no in range(no_lines+1):
    if len(text)<words_per_line:
        line=text
        lines.append(line)
        new_text="".join(lines)
        return new_text,len(lines)
    line,words_per_line=check_last_space(words_per_line,text)
    text=text.replace(text[:words_per_line],"")
    words=line.split()
    line=" ".join(words)
    line=line+"\n"
    lines.append(line)
    words_per_line=38
    
def get_profile_name_score(profile_name):
  score=0
  for i in profile_name:
    if i in string.punctuation:
      score=score+0.2
    elif i in [" "]:
      score=score+0.5
    else:
      score=score+1
  return score
  
          
def create_screenshot(text,profile_pics,username,profile_name,user_verified=False):
  text,no_lines=clean_text(text)
  print(text)
  profile_name_score=get_profile_name_score(profile_name)
  width=1400
  border_top_bottom=120
  space_text=45*no_lines*1.8
  space_profile=186
  total_height=int(space_text+2*border_top_bottom+space_profile)
  img= Image.new(mode="RGB", size=(width,total_height),color=(256,256,256))
  drawer=ImageDraw.Draw(img)
  drawer_emoji=Pilmoji(img)
  font=ImageFont.truetype("OpenSans-Regular.ttf",70)
  font_username=ImageFont.truetype("OpenSans-Regular.ttf",45)
  bold_font=ImageFont.truetype("Roboto-Bold.ttf",50)
  # Add Text to image
  drawer_emoji.text((70, 305), text, font=font,fill=(0,0,0),embedded_color=True,emoji_scale_factor=1.1, emoji_position_offset=(10,15))
  drawer.text((240,130),user,font=bold_font,fill=(0,0,0))
  drawer.text((240,185), username,font=font_username,fill=(134, 135, 134))
  img.paste(profile_pics, (70, 120), mask_im)
  if user_verified==True:
  	img.paste(verified,(int(240+28*(profile_name_score)),140))
  return img
 
 
 
 
def create_screenshot_dark(text,profile_pics,username,profile_name,user_verified=False):
  text,no_lines=clean_text(text)
  print(text)
  profile_name_score=get_profile_name_score(profile_name)
  width=1400
  border_top_bottom=120
  space_text=45*no_lines*1.8
  space_profile=186
  total_height=int(space_text+2*border_top_bottom+space_profile)
  img= Image.new(mode="RGB", size=(width,total_height),color=(0,0,0))
  drawer=ImageDraw.Draw(img)
  drawer_emoji=Pilmoji(img)
  font=ImageFont.truetype("OpenSans-Regular.ttf",70)
  font_username=ImageFont.truetype("OpenSans-Regular.ttf",45)
  bold_font=ImageFont.truetype("Roboto-Bold.ttf",50)
  # Add Text to image
  drawer_emoji.text((70, 305), text, font=font,fill=(255, 255, 255),embedded_color=True,emoji_scale_factor=1, emoji_position_offset=(10,15))
  drawer.text((240,130),user,font=bold_font,fill=(255, 255, 255))
  drawer.text((240,185), username,font=font_username,fill=(196, 195, 194))
  img.paste(profile_pics, (70, 120), mask_im)
  if user_verified==True:
  	img.paste(verified_dark,(int(240+28*(profile_name_score)),128))
  return img
user="David Effiong"
username="@DavidEffiong16"
img=create_screenshot_dark(text,profile_pics, username,user,user_verified=True)
img.save("pictured.jpg")
plt.imshow(img)
plt.show()