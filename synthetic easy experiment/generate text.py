from PIL import ImageFont, ImageDraw, Image
import random
import string
import json
import os
from pathlib import Path

p = Path('./fonts/')
fontfiles = list(p.glob('Roboto-Bold.ttf'))

genes = []
f = open("hgnc_complete_set.json", 'r', encoding="utf8")
data = json.loads(f.read())
f.close()
for x in data['response']['docs']:
    genes.append(x['symbol'])

# use a truetype font
fonts = []
# for i in range(10, 33):
    # for f in fontfiles:
        # fonts.append(ImageFont.truetype(str(f), i))
# add fonts at 24 point
for f in fontfiles:
    fonts.append(ImageFont.truetype(str(f), 24))

def getGene():
    return random.choice(genes)

def createString():
    text = random.choices(string.ascii_letters + string.digits + '-', k=7)
    text = "".join(text)
    return text

def randomColor():
    colors = [0, 64, 128, 191, 255]
    return (random.choice(colors), random.choice(colors), random.choice(colors))

def realFontbbox(fontBBox):
    l = []
    for x in fontBBox:
        l.append(x + 32)
    return l

def shapeBoundingBox(fontBBox):
    return [fontBBox[0] - random.choice(range(0,11)), fontBBox[1] - random.choice(range(0,11)),
            fontBBox[2] + random.choice(range(0,12)), fontBBox[3] + random.choice(range(0,12))]

def cropBoundingBox(fontBBox):
    return [fontBBox[0] - random.choice(range(-3,16)), fontBBox[1] - random.choice(range(-3,16)),
            fontBBox[2] + random.choice(range(-3,16)), fontBBox[3] + random.choice(range(-3,16))]

def simpleCropBoundingBox(fontBBox):
    return [fontBBox[0] - 5, fontBBox[1] - 5,
            fontBBox[2] + 5, fontBBox[3] + 5]

def createImage(text):
    font = random.choice(fonts)
    fontColor = randomColor()
    backgroundColor = randomColor()
    while backgroundColor == fontColor:
        backgroundColor = randomColor()
    shapeColor = randomColor()
    while shapeColor == fontColor:
        shapeColor = randomColor()
    shapeBorderColor = randomColor()
    fontbbox = font.getbbox(text)
    fontbbox = realFontbbox(fontbbox)
    shapebbox = shapeBoundingBox(fontbbox)
    #cropbbox = cropBoundingBox(fontbbox)
    #crop 5 pixels outside text bbox
    cropbbox = simpleCropBoundingBox(fontbbox)
    #image = Image.new("RGB", (256, 256), backgroundColor)
    # white background
    image = Image.new("RGB", (512, 512), (255,255,255))
    draw = ImageDraw.Draw(image)
    shape = random.choice(range(3))
    shapeBorderSize = random.choice(range(6))
    # skip 0 for no shape
    shape = 0 # no shape for simple test images
    if shape == 1:
        draw.rectangle(shapebbox, shapeColor, shapeBorderColor, shapeBorderSize)
    if shape == 2:
        draw.ellipse(shapebbox, shapeColor, shapeBorderColor, shapeBorderSize)

    #draw.text((32, 32), text, font=font, fill=fontColor)
    #black text
    draw.text((32, 32), text, font=font, fill=(0,0,0))

    realImage = image.crop(cropbbox)
    return realImage

num = 1000
loc = "train"
gt = open(loc + "_label.json", 'w')
os.mkdir(loc+"_imgs/")

jpegQualityLevels = [50, 75, 95, 100]

for i in range(num):
    if i % (num/100) == 0:
        print(str((i/num)*100) + "%")
    #text = createString() # random
    text = getGene() # gene name/symbol
    img = createImage(text)
    imgFilename = str(i) + ".jpg"
    imgPath = loc + "_imgs/" + imgFilename
    # https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil
    #img.save(imgPath, optimize=True, quality=random.choice(jpegQualityLevels))
    img.save(imgPath)
    data = {"filename":imgFilename, "text":text}
    jsonData = json.dumps(data)
    gt.write(jsonData + "\n")

gt.close()
