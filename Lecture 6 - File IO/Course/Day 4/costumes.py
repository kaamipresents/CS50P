import sys

from PIL import Image

images = []

for arg in sys.argv[1:]:
    im = Image.open(arg)
    images.append(im)

images[0].save('out.gif', save_all=True, append_images=[images[1]], duration=200, loop=0, optimize=True)