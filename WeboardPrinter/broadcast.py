from main import *
from PIL import Image
import time
import random
import win32gui
import win32ui
import win32con
import win32api

global width, height
alpha = 30
width = alpha * 16
height = alpha * 9


def init_array():
    global pix
    pix = []
    for i in range(width):
        tmp = []
        for j in range(height):
            tmp.append((0, 0, 0))
        pix.append(tmp)


def get_screen(filename):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    moniterDev = win32api.EnumDisplayMonitors(None, None)
    w = moniterDev[0][2][2]
    h = moniterDev[0][2][3]
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


def update_pixel(filename):
    img = Image.open(filename)
    img = img.resize((width, height), Image.ANTIALIAS)
    global buf
    buf = []
    for x in range(width):
        for y in range(height):
            p = img.getpixel((x, y))
            if abs(p[0] - pix[x][y][0]) + abs(p[1] - pix[x][y][1]) + abs(p[2] - pix[x][y][2]) > 5:
                buf.append((x, y, p[0], p[1], p[2]))


def flush_dirty():
    global buf
    global pix
    #   random.shuffle(buf)
    for data in buf:
        x = data[0]
        y = data[1]
        r = data[2]
        g = data[3]
        b = data[4]
        pix[x][y] = (r, g, b)
        draw(x, y, r, g, b)


screen_buffer_path = "screen.jpg"
init_array()
t = 0
while True:
    t += 1
    print("SnapShot " + str(t))
    get_screen(screen_buffer_path)
    update_pixel(screen_buffer_path)
    flush_dirty()
    time.sleep(0.10)
