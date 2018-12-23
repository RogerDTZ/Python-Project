import time
import msvcrt

from pip._vendor.distlib.compat import raw_input

from main import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def init_webdriver():
    global driver
    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=d)
    #   driver = webdriver.Chrome()
    driver.get("http://192.168.63.158/")
    driver.implicitly_wait(5)
    time.sleep(1)


def init_array():
    global on, info
    on = []
    info = []
    for i in range(1280):
        tmp1 = []
        tmp2 = []
        for j in range(720):
            tmp1.append(False)
            tmp2.append((0, 0, 0))
        on.append(tmp1)
        info.append(tmp2)


def get_pixel(x, y):
    js = "var buf=context.getImageData({},{},1,1).data; console.log(String(buf[0]+1000)+String(buf[1]+1000)+String(buf[2]+1000))".format(
        x, y)
    driver.execute_script(js)
    r = g = b = 0
    for entry in driver.get_log('browser'):
        l = len(entry['message'])
        s = entry['message'][l - 13:l]
        r = int(s[0:4]) - 1000
        g = int(s[4:8]) - 1000
        b = int(s[8:12]) - 1000
    driver.execute_script("console.clear();")
    return r, g, b


def on_enter_pixel(x, y):
    if on[x][y]:
        return
    on[x][y] = True
    info[x][y] = get_pixel(x, y)


def on_exit_pixel(x, y):
    if not on[x][y]:
        return
    on[x][y] = False
    draw(x, y, info[x][y][0], info[x][y][1], info[x][y][2], False)


def draw_circle(x, y, r1, r2, r, g, b):
    for i in range(x - r2, x + r2 + 1):
        for j in range(y - r1, y + r2 + 1):
            if 0 <= i < 1280 and 0 <= j < 720:
                if r1 <= (i - x) * (i - x) + (j - y) * (j - y) <= r2:
                    #   on_enter_pixel(i, j)
                    draw(i, j, r, g, b, False)
                else:
                    pass
                    #   on_exit_pixel(i, j)


def prod():
#	init_webdriver()
    init_array()
    curx = random.randint(0, 200)
    cury = random.randint(0, 200)
    nr = random.randint(0, 255)
    ng = random.randint(0, 255)
    nb = random.randint(0, 255)
    while True:
        ch = str(msvcrt.getch())
        #   curx += random.randint(-1, 1)
        #   cury += random.randint(-1, 1)
        if ch[2:3] == 'w':
            cury -= 3
        elif ch[2:3] == 's':
            cury += 3
        elif ch[2:3] == 'a':
            curx -= 3
        elif ch[2:3] == 'd':
            curx += 3
        curx = max(curx, 0)
        curx = min(curx, 1280)
        cury = max(cury, 0)
        cury = min(cury, 720)
        nr += random.randint(-5, 5)
        ng += random.randint(-5, 5)
        nb += random.randint(-5, 5)
        nr = (nr + 256) % 256
        ng = (ng + 256) % 256
        nb = (nb + 256) % 256
        print(str(curx) + " " + str(cury))
        draw_circle(curx, cury, 10, 200, nr, ng, nb)
