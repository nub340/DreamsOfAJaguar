from PIL import Image, ImageOps

img = Image.open("graphics/imported_units/bird.1.3.png")
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    if (item[0] >= 240 and item[1] >= 240 and item[2] >= 240):
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
newsize = (128, 128)
img = img.resize(newsize)
img.save("graphics/imported_units/result4.png", "PNG")

