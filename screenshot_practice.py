import re
import emoji
import string
import numpy as np
from pilmoji import Pilmoji
from PIL import Image, ImageFont, ImageDraw

verified = Image.open("verified.png")
verified = verified.convert("RGB")
verified = verified.resize((45, 45))

verified_dark = Image.open("verified_dark.png")
verified_dark = verified_dark.convert("RGB")
verified_dark = verified_dark.resize((60, 60))


def check_last_space(last_index, text):
    try:
        while last_index > 1:
            if text[last_index] != " ":
                last_index = last_index - 1
            else:
                return text[:last_index], last_index
    except:
        return text, len(text)


def remove_start_space(line):
    if line[:2] == "  ":
        line = line[2 : len(line)]
    elif line[0] == " ":
        line = line[1 : len(line)]
    return line


def clean_text(text):
    words_per_line = 46
    no_lines = (len(text) // words_per_line) + 1
    lines = []
    for line_no in range(no_lines + 1):
        if len(text) < words_per_line:
            line = text
            line = remove_start_space(line)
            lines.append(line)
            new_text = "".join(lines)
            return new_text, len(lines)
        line, words_per_line = check_last_space(words_per_line, text)
        text = text.replace(text[:words_per_line], "")
        words = line.split()
        line = " ".join(words)
        line = remove_start_space(line)
        line = line + "\n"
        lines.append(line)
        words_per_line = 46


def find_n(text):
    text_split = text.split("\n")
    new_text = ""
    total_lines = 0
    for txt in text_split:
        if txt == "":
            new_text = new_text + "\n"
            total_lines = total_lines + 1
        else:
            txt_lines, no_lines = clean_text(txt)
            new_text = new_text + txt_lines + "\n"
            total_lines = total_lines + no_lines
    new_text = re.sub("http[s]?://\S+", "", new_text)
    return new_text, total_lines


text = "Things you need to share before you start dating:\n1. HIV Status\n2. Any illnesses or mental disorders\n3. Criminal record status\n4. If you have kids\n5. One's attitude towards Bushiri\n6. History of abortions\n7. Relationship Status\n8. Credit Record\n9. Political Party \n10. Occupation"


def get_profile_name_score(profile_name):
    score = 0
    for i in profile_name:
        if i in string.punctuation:
            score = score + 0.2
        elif i in [" "]:
            score = score + 0.5
        elif i in string.ascii_uppercase:
            score = score + 1.24
        else:
            score = score + 1
    return score


def get_profile_pics_mask(profile_pics):
    h, w = profile_pics.size
    lum_img = Image.new("L", [h, w], 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0, 0), (h, w)], 0, 360, fill=255)
    img_arr = np.array(profile_pics)
    lum_img_arr = np.array(lum_img)
    mask_im = Image.fromarray(lum_img_arr)
    profile_pics = profile_pics.resize((130, 130))
    mask_im = mask_im.resize((130, 130))
    return profile_pics, mask_im


def create_screenshot_light(
    text, profile_pics, username, profile_name, date, user_verified=False
):
    text, no_lines = find_n(text)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    username = "@" + username
    width = 1300
    border_top_bottom = 120
    space_text = 45 * no_lines * 1.6
    space_profile = 186
    date_height = int(space_text + border_top_bottom + space_profile + 5)
    total_height = int(space_text + 2 * border_top_bottom + space_profile)
    img = Image.new(mode="RGB", size=(width, total_height), color=(256, 256, 256))
    drawer = ImageDraw.Draw(img)
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 55)
    font_username = ImageFont.truetype("OpenSans-Regular.ttf", 45)
    bold_font = ImageFont.truetype("Roboto-Bold.ttf", 50)
    # Add Text to image
    drawer_emoji.text(
        (70, 305),
        text,
        font=font,
        fill=(0, 0, 0),
        embedded_color=True,
        emoji_scale_factor=1.1,
        emoji_position_offset=(10, 15),
    )
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(0, 0, 0))
    drawer.text((240, 185), username, font=font_username, fill=(134, 135, 134))
    drawer.text((70, date_height), date, font=font_username, fill=(134, 135, 134))
    img.paste(profile_pics, (70, 120), mask)
    if user_verified == True:
        img.paste(verified, (int(240 + 28.15 * (profile_name_score)), 140))
    return img


def create_screenshot_dark(
    text, profile_pics, username, profile_name, date, user_verified=False
):
    text, no_lines = find_n(text)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    username = "@" + username
    width = 1300
    border_top_bottom = 120
    space_text = 45 * no_lines * 1.6
    space_profile = 186
    date_height = int(space_text + border_top_bottom + space_profile + 5)
    total_height = int(space_text + 2 * border_top_bottom + space_profile)
    img = Image.new(mode="RGB", size=(width, total_height), color=(0, 0, 0))
    drawer = ImageDraw.Draw(img)
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 55)
    font_username = ImageFont.truetype("OpenSans-Regular.ttf", 45)
    bold_font = ImageFont.truetype("Roboto-Bold.ttf", 50)
    # Add Text to image
    drawer_emoji.text(
        (70, 305),
        text,
        font=font,
        fill=(255, 255, 255),
        embedded_color=True,
        align="left",
        emoji_scale_factor=1,
        emoji_position_offset=(10, 15),
    )
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(255, 255, 255))
    drawer.text((240, 185), username, font=font_username, fill=(196, 195, 194))
    drawer.text((70, date_height), date, font=font_username, fill=(196, 195, 194))
    img.paste(profile_pics, (70, 120), mask)
    if user_verified == True:
        img.paste(verified_dark, (int(240 + 28.15 * (profile_name_score)), 128))
    return img
