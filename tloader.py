import base64
from io import BytesIO
import sys
import os
from PIL import Image
from selenium import webdriver

if not(os.path.exists("chromedriver.exe")):
    print("no chromedriver")
    sys.exit(1)

options = webdriver.ChromeOptions()
options.add_argument("--test-type")
options.add_argument("--disable-web-security")
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

def decode_img(img_data, filename):
    splited = img_data.split(',')[1]
    im = Image.open(BytesIO(base64.b64decode(splited)))
    print("Saving image " + filename + ".png   ...")
    im.save(filename + ".png")

def inition(uri):
    driver.get(uri)

def getimage(imgid, filename):
    base64 = driver.execute_script("var c = document.createElement('canvas'); var ctx = c.getContext('2d'); var img = document.getElementById('" + imgid + "'); c.height=img.height; c.width=img.width; ctx.drawImage(img, 0, 0,img.width, img.height); var base64String = c.toDataURL(); return base64String;")
    decode_img(base64, filename)

i = 0
try:
    inition(sys.argv[1])
except:
    print("no arguments")
    driver.quit()
    sys.exit(1)

while(1):
    try:
        getimage("content_image_" + str(i), "tmp/" + str(i+1))
        i = i + 1
    except:
        break
        print('done!')
        driver.quit()
        sys.exit(0)
