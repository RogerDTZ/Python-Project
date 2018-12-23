import websocket
import random
from PIL import Image


def connect_website(website_url):
	global ws
	ws = websocket.WebSocket()
	ws.connect(website_url)


def draw_pixel(x, y, r, g, b, flit_white=False):
	if flit_white:
		if r>=250 and g>=250 and b>=250:
			return
	global ws
	ws.send(str(x)+"|"+str(y)+"|"+str(r)+"|"+str(g)+"|"+str(b))
	#   value = int(r / 256.0 * 6) * 36 + int(g / 256.0 * 6) * 6 + int(b / 256.0 * 6)
	#   ws.send("DRAW|" + str(x) + "|" + str(y) + "|" + str(value))


def fill_rect(x, y, width, height, r, g, b, emerge=False):
	pos = []
	for x in range(x, x+width):
		for y in range(y, y+height):
			pos.append((x, y))
	if emerge:
		random.shuffle(pos)
	for pos in pos:
		draw_pixel(pos[0], pos[1], r, g, b)


def print_image(image_path, x, y, emerge=False, flit_white=False):
	img = Image.open("image/"+image_path)
	width = img.width
	height = img.height
	pix = []
	for x in range(width):
		for y in range(height):
			pix.append((x, y))
	if emerge:
		random.shuffle(pix)
	for pos in pix:
		p = img.getpixel((pos[0], pos[1]))
		draw_pixel(x+pos[0], y+pos[1], p[0], p[1], p[2], flit_white)


def play_gif(gif_name, frame_range, x, y, emerge=False, flit_white=False):
	while True:
		print("Drawing "+gif_name)
		for i in range(frame_range):
			name = str(i)
			if i<10:
				name = "0"+name
			if i<100:
				name = "0"+name
			print_image(gif_name+"/"+gif_name+name+".jpg", x, y, emerge, flit_white)
			print("{}/{}".format(i+1, frame_range))


connect_website("ws://192.168.63.158:1919")
#   connect("ws://www.tatsu68.com/pixelboard/server")
