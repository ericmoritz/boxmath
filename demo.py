from wand import image
from boxmath import *

FILTER="gaussian"

def load():
    return image.Image(filename="chrysanthemum.jpg")


def chained():
    i = load()
    i.resize(629, 483, filter=FILTER)
    i.crop(0, 0, 480, 480)
    i.resize(1000, 1000, filter=FILTER)
    i.save(filename="flower-chained.jpg")


def mb():
    i = load()
    b = box(i.width, i.height)
    b = resize(b, 629, 483)
    b = crop(b, 0, 0, 480, 480)
    b = resize(b, 1000, 1000)

    def resizer(img, w, h):
        img.resize(int(w), int(h), filter=FILTER)
        return img

    def cropper(img, l,t,r,b):
        img.crop(int(l),int(t),int(r),int(b))
        return img

    t = make_transformer(b, resizer, cropper)
    i = t(i)
    i.save(filename="flower-boxmath.jpg")

def main():
    chained()
    mb()

if __name__ == '__main__':
    main()
