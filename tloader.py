#tLoader for naver webtoon 2018-08-13
#By lill74

import os
import sys
import base64
import multiprocessing
from io import BytesIO
from PIL import Image
from selenium import webdriver

title = ""
fpath = ""
subtitle = ""
author = ""

count = 0
maxpg = 0

if not os.path.exists("chromedriver.exe"):
    print("no chromedriver")
    sys.exit(1)

if len(sys.argv) <= 1:
    print("no arguments")
    sys.exit(1)

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument("--test-type")
options.add_argument("--disable-web-security")

driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

def decodeImg(b64data, fname):
    if not os.path.exists(fpath):
        print("Creating directories")
        os.makedirs(fpath)

    img = Image.open(BytesIO(base64.b64decode(b64data.split(',')[1])))
    print(title + " " + subtitle + " Saving  .. (" + str(count) + " / " + str(maxpg) + ")" )
    img.save(fname + ".png")

def getimg(imgid, fname):
    b64data = driver.execute_script("var c = document.createElement('canvas'); var ctx = c.getContext('2d'); var img = document.getElementById('" + imgid + "'); c.height=img.height; c.width=img.width; ctx.drawImage(img, 0, 0,img.width, img.height); var base64String = c.toDataURL(); return base64String;")
    decodeImg(b64data, fname)

def getpage(uri):
    global title
    global subtitle
    global author
    global fpath
    global maxpg

    driver.get(uri)

    tmptitle = driver.find_element_by_class_name("detail").find_element_by_tag_name("h2")
    maxpg = len(driver.find_element_by_class_name("wt_viewer").find_elements_by_tag_name("img"))
    author = tmptitle.find_element_by_tag_name("span").text
    title = tmptitle.text.replace(" " + author , "")
    subtitle = driver.find_element_by_class_name("view").find_element_by_tag_name("h3").text
    fpath = title + "\\" + subtitle

    print(title + " " + subtitle)

    for i in range(0, maxpg):
        global count

        count = i
        getimg("content_image_" + str(i), fpath + "\\" + str(i + 1))

    print(title + " " + subtitle + " Done!")
    driver.close()

def main():
    if(len(sys.argv) == 2):
        getpage(sys.argv[1])
    elif(len(sys.argv) == 3):
        splited = sys.argv[2].split("-")
        if(len(splited) == 1):
            getpage(sys.argv[1] + sys.argv[2])
        elif(len(splited) == 2):
            for j in range(int(splited[0]), int(splited[1]) + 1):
                proc = multiprocessing.Process(target=getpage, args=((sys.argv[1] + str(j)),))
                proc.start()

                if int(j%5) == 0:
                    proc.join()
                
        else:
            print("argument error")
            driver.quit()
            sys.exit(1)
    else:
        print("argument error")
        driver.quit()
        sys.exit(1)

    driver.quit()
    sys.exit(0)


def rt(dd):
    return dd

if __name__ == "__main__":
    main()
