import time
import random
from selenium import webdriver
from PIL import Image

lis = {'0': "#000000",
       '1': "#ffffff",
       '2': "#aaaaaa",
       '3': "#555555",
       '4': "#fed3c7",
       '5': "#ffc4ce",
       '6': "#faac8e",
       '7': "#ff8b83",
       '8': "#f44336",
       '9': "#e91e63",
       'A': "#e2669e",
       'B': "#9c27b0",
       'C': "#673ab7",
       'D': "#3f51b5",
       'E': "#004670",
       'F': "#057197",
       'G': "#2196f3",
       'H': "#00bcd4",
       'I': "#3be5db",
       'J': "#97fddc",
       'K': "#167300",
       'L': "#37a93c",
       'M': "#89e642",
       'N': "#d7ff07",
       'O': "#fff6d1",
       'P': "#f8cb8c",
       'Q': "#ffeb3b",
       'R': "#ffc107",
       'S': "#ff9800",
       'T': "#ff5722",
       'U': "#b83f27",
       'V': "#795548"}


def connect_website():
    global driver
    driver = webdriver.Chrome()
    driver.get("https://board.mcfx.us/")
    driver.implicitly_wait(3)
    time.sleep(1)


def trans(c):
    if ord(c) >= ord('a'):
        return 10 + (ord(c) - ord('a'))
    else:
        return ord(c) - ord('0')


def get_rgb(s):
    r = trans(s[1:2]) * 16 + trans(s[2:3])
    g = trans(s[3:4]) * 16 + trans(s[4:5])
    b = trans(s[5:6]) * 16 + trans(s[6:7])
    return r, g, b


def get_color(r, g, b):
    global lis
    min_dis = 100000
    min_who = -1
    for p in lis:
        tmp = get_rgb(lis[p])
        dis = abs(tmp[0] - r) + abs(tmp[1] - b) + abs(tmp[2] - g)
        if dis < min_dis:
            min_dis = dis
            min_who = p
    return min_who


def draw_pixel(x, y, r, g, b, flit):
    if flit:
        if r >= 250 and g >= 250 and b >= 250:
            return
    driver.execute_script("$.post('/draw',{{x:{}+{}*1280,v:{}}})".format(x, y, get_color(r, g, b)))


def print_image(path, dx, dy, shuffled, flit):
    img = Image.open(path)
    width = img.width
    height = img.height
    pix = []
    for x in range(width):
        for y in range(height):
            pix.append((x, y))
    if shuffled:
        random.shuffle(pix)
    for pos in pix:
        p = img.getpixel((pos[0], pos[1]))
        draw_pixel(dx + pos[0], dy + pos[1], p[0], p[1], p[2], flit)


connect_website()
#   draw_pixel(0, 0, 0, 0, 0)
