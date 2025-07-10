from PIL import Image

img = Image.open('example.jpg')

gray_img = img.convert('L')
gray_img.save('gray_example.jpg')