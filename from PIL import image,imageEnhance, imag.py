from PIL import Image, ImageEnhance, ImageFilter
import os

path = './imgs'
pathOut = '/editedImgs'

for filename in os.listdir(path):
    img = Image.open(f"{path}/{filename}")

    edit = img.filter(ImageFilter.SHARPEN).rotate(90)
    edit = enhancer.enhance(factor)
    
    factor = 1.5
    
    enhancer = ImageEnhance.contrast(edit)
    clean_name = os.path.splitext(filename)[0]
    edit.save(f'.{pathOut}/{clean_name}_edited.jpg')