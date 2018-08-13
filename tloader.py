#tLoader for naver webtoon 2018-08-13
#By lill74

import sys
import base64
import os
from io import BytesIO
from PIL import Image
from selenium import webdriver

title = ""
subtitle = ""
author = ""
fpath = ""
maxpg = 0
count = 0

if not os.path.exists("chromedriver.exe"):
    print("no chromedriver")
    sys.exit(1)

if len(sys.argv) <= 1:
    print("no arguments")
    sys.exit(1)

options = webdriver.ChromeOptions()
options.add_argument("--test-type")
options.add_argument("--disable-web-security")

driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)


def progress(val, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * val / float(total)))

    percents = round(100.0 * val / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ... %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()  # As suggested by Rom Ruben (see: http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/27871113#comment50529068_27871113)

def decodeImg(b64data, fname):
    if not os.path.exists(fpath):
        print("Creating directories")
        print(fpath)
        os.makedirs(fpath)

    img = Image.open(BytesIO(base64.b64decode(b64data.split(',')[1])))
    progress(count + 1, maxpg, "(" + str(count) + "/" + str(maxpg) + ")")
    img.save(fname + ".png")

def getimg(imgid, fname):
    b64data = driver.execute_script("var c = document.createElement('canvas'); var ctx = c.getContext('2d'); var img = document.getElementById('" + imgid + "'); c.height=img.height; c.width=img.width; ctx.drawImage(img, 0, 0,img.width, img.height); var base64String = c.toDataURL(); return base64String;")
    decodeImg(b64data, fname)

#uri format https://comic.naver.com/webtoon/detail.nhn?titleId=622644&no=171
def getpage(uri):
    global title
    global subtitle
    global author
    global fpath
    global maxpg
    global count

    driver.get(uri)

    tmptitle = driver.find_element_by_class_name("detail").find_element_by_tag_name("h2")
    maxpg = len(driver.find_element_by_class_name("wt_viewer").find_elements_by_tag_name("img"))
    author = tmptitle.find_element_by_tag_name("span").text
    title = tmptitle.text.replace(" " + author , "")
    subtitle = driver.find_element_by_class_name("view").find_element_by_tag_name("h3").text
    fpath = title + "\\" + subtitle

    print(title + " " + subtitle)

    for i in range(0, maxpg):
        count = i
        getimg("content_image_" + str(i), fpath + "\\" + str(i + 1))

    print("Done!")
    driver.quit()

getpage(sys.argv[1])
