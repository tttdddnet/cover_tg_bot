# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops, ImageColor, ImageEnhance
from webpreview import webpreview
import textwrap
import random
import sys
import requests
import shutil
import os


def get_preview_url(link):
    preview = webpreview(link)
    return preview.image


def get_templates_with_frog():
    templates = []
    path = 'templates/'
    for file in os.listdir(path):
        if file.endswith(".png"):
            templates.append(os.path.join(path, file))
    return templates

def open_templates_with_frog():
    templates = get_templates_with_frog()
    template = Image.open(random.choice(templates))
    return template


def save_preview(link):
    try:
        preview_url = get_preview_url(link)
        file_name = 'preview.jpg'
        res = requests.get(preview_url, stream=True)
        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            image = Image.open("preview.jpg")
            return image
    except:
        image = Image.open("/home/template.jpg")
    return image


def scale_and_crop_preview(link):
    image = save_preview(link)
    image = image.convert('RGB')
    image_width, image_height = image.size
    if image_width / image_height < 2:
        image = ImageOps.contain(image, (1000, image_height))
        width, height = image.size
        height_of_one_bar = (height - 500) / 2
        x0 = 0
        y0 = height_of_one_bar
        x1 = width
        y1 = height - height_of_one_bar
        image = image.crop((x0, y0, x1, y1))
    else:
        image = ImageOps.contain(image, (image_width, 500))
        width, height = image.size
        width_of_one_bar = (width - 1000) / 2
        x0 = width_of_one_bar
        y0 = 0
        x1 = width - width_of_one_bar
        y1= height

        image = image.crop((x0, y0, x1, y1))
    return image

def enhance_image(link):
    image = scale_and_crop_preview(link)
    image = ImageEnhance.Brightness(image)
    factor = 0.30 #меньше - темнее
    image = image.enhance(factor)
    image.save("enhance_image.jpg", subsampling=0, quality=100)
    return image


def draw_text_and_save_image(text, link):
    font_size = 60
    image = enhance_image(link)
    font = ImageFont.truetype("/home/RG-StandardBoldItalic.ttf", font_size)

    drawer = ImageDraw.Draw(image)

    # отступ слева
    margin = 35
    # отступ сверху
    offset = 150
    # width — длина строки {размер ширифта:длина строки}, шаг 0.8
    step = 0.8
    line_width0 = 29
    width = {font_size:(line_width0)}
    full_width = font.getlength(text)
    for line in textwrap.wrap(text, width=int(width[font_size])):
        line_width = font.getlength(line)
        left, top, right, bottom = drawer.multiline_textbbox((line_width-full_width, offset), text, font=font)
        drawer.rectangle((left - 50, top - 8, right + 65, bottom + 8), fill=(55, 143, 246))
        drawer.text((margin, offset), line, font=font, fill=(255, 255, 255))
        offset += 68

    return image


def insert_proglib_logo(text, link):
    image = draw_text_and_save_image(text, link)
    proglib_logo = Image.open("/home/proglib.png")
    image.paste(proglib_logo, (45, 35), mask=proglib_logo)
    image.save('image_with_logo.jpg', subsampling=0, quality=100)
    return image


def draw_tag(text, link, tag):
    image = insert_proglib_logo(text, link)
    drawer = ImageDraw.Draw(image)

    font_size = 28
    font = ImageFont.truetype("/home/RG-StandardBold.ttf",  font_size)

    def draw_video_tag():
        text = '#видео'
        drawer.text((865, 40), text, font=font, fill='white', align="left")

    def draw_instruments_tag():
        text = '#инструменты'
        drawer.text((772, 40), text, font=font, fill='white', align="left")

    def draw_post_tag():
        text = '#простопост'
        drawer.text((800, 40), text, font=font, fill='white', align="left")

    def draw_podcast_tag():
        text = '#подкасты'
        drawer.text((818, 40), text, font=font, fill='white', align="left")

    if tag == 'tools':
        draw_instruments_tag()
    elif tag == 'video':
        draw_video_tag()
    elif tag == 'just post':
        draw_post_tag()
    elif tag == 'podcast':
        draw_podcast_tag()


    image.save('image_with_tag.jpg', subsampling=0, quality=100)
    return image

