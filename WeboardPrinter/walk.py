import main
import random
import time
import circle
from PIL import Image

global flipx, flipy, now
flipx = False
flipy = False
now = 0


def print_image(path, px, py):
    img = Image.open(path)
    width = img.width
    height = img.height
    pix = []
    for dx in range(width):
        for dy in range(height):
            pix.append((dx, dy))
    for pos in pix:
        p = img.getpixel((pos[0], pos[1]))
        if not flipx:
            main.draw(px + pos[0], py + pos[1], p[0], p[1], p[2], False)
        else:
            main.draw(px + width - pos[0], py + pos[1], p[0], p[1], p[2], False)


def print_gif(path, num):
    global x, y, now
    print("Drawing")
    for i in range(num):
        name = str(i)
        if i < 10:
            name = "0" + name
        if i < 100:
            name = "0" + name
        print_image("image/" + path + "/" + path + name + ".jpg", x, y)
        now += 1
        #   if now % 20 < 10:
        #   circle.draw_circle(x + 15, y + 16, 200, 220, 255, 238, 19)
        print("{}/{}".format(i + 1, num))
        time.sleep(0.05)
        main.fill(x-1,y,33,2,255,255,255,False)
        main.fill(x-1,y+31,33,2,255,255,255,False)
        change()


def change():
    global x, y, flipx, flipy
    if not flipx:
        x += random.randint(1, 2)
    else:
        x -= random.randint(1, 2)
    if not flipy:
        y += random.randint(1, 2)
    else:
        y -= random.randint(1, 2)
    if x < 50:
        flipx ^= 1
        x = 50
    if x > 1230:
        flipx ^= 1
        x = 1230
    if y < 50:
        flipy ^= 1
        y = 50
    if y > 670:
        flipy ^= 1
        y = 670
    if random.randint(0, 80) == 0:
        flipx ^= 1
    if random.randint(0, 80) == 0:
        flipy ^= 1


def play_gif(path, frame, sx, sy):
    global x, y
    x = sx
    y = sy
    while True:
        print_gif(path, frame)


play_gif("xfzwalk", 19, random.randint(50, 1230), random.randint(50, 670))
