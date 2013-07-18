import pytest
from boxmath import model
from boxmath.model import size
from fractions import Fraction
from testfixtures import compare

def tmodel(w,h):
    return (0,0,w,h)


def tresize(w,h,m):
    l,t,r,b = m
    w0 = r - l
    h0 = b - t
    ws = Fraction(w, w0)
    hs = Fraction(h, h0)
    return (l*ws, t*hs, r*ws, b*hs)


def tcrop(crop, m):
    l,t,r,b = crop
    l0,t0,r0,b0 = m
    return (l0+l, t0+t, l0+r, t0+b)


def get_percent(total, percent):
    return int(
        total * percent / 100.0
    )


def half(num):
    return Fraction(num, 2)


def double(num):
    return num * 2


MAX=1000

def choose(percent, bottom, top):
    pct = (percent % 100) / 100.0
    span = top - bottom
    return int(bottom + span * pct)


@pytest.mark.randomize(w=int,h=int, w1=int, h1=int, min_num=1, max_num=MAX)
@pytest.mark.randomize(lp=int, tp=int, rp=int, bp=int, min_num=0, max_num=100)
def test_crop_resize(w,h,w1,h1,lp,tp,rp,bp):
    l = choose(lp, 1, w)
    t = choose(tp, 1, h)
    r = choose(rp, l, w)
    b = choose(bp, t, h)
    l,r = sorted([l,r])
    t,b = sorted([t,b])

    # ignore 0 sized crops
    if l == r or t == b:
        return

    
    box = model.resize(
        model.crop(
            model.box(w, h),
            l,t,r,b,
        ),
        w1, h1
    )

    def resize_cb(i, w, h):
        return tresize(w,h,i)

    def crop_cb(i, l,t,r,b):
        return tcrop((l,t,r,b),i)

    f = model.make_transformer(box, resize_cb, crop_cb)
    x = f(tmodel(w,h))

    m = tresize(
        w1, h1,
        tcrop(
            (l,t,r,b),
            tmodel(w,h)
       )
    )

    print box
    compare(m,x)

@pytest.mark.randomize(w=int,h=int, w1=int, h1=int, min_num=1, max_num=MAX)
@pytest.mark.randomize(lp=int, tp=int, rp=int, bp=int, min_num=0, max_num=100)
def test_resize_crop(w,h,w1,h1,lp,tp,rp,bp):
    l = choose(lp, 1, w1)
    t = choose(tp, 1, h1)
    r = choose(rp, l, w1)
    b = choose(bp, t, h1)
    l,r = sorted([l,r])
    t,b = sorted([t,b])

    # ignore 0 sized crops
    if l == r or t == b:
        return

    
    box = model.crop(
        model.resize(
            model.box(w, h),
            w1, h1
        ),
        l,t,r,b,
    )

    def resize_cb(i, w, h):
        print map(int, [w,h])
        return tresize(w,h,i)

    def crop_cb(i, l,t,r,b):
        print map(int, [l,t,r,b])
        return tcrop((l,t,r,b),i)

    f = model.make_transformer(box, resize_cb, crop_cb)
    x = f(tmodel(w,h))

    m = tcrop(
        (l,t,r,b),
        tresize(
            w1, h1,
            tmodel(w,h)
       )
    )

    print (w,h,l,t,r,b,w1,h1)
    compare(m,x)

@pytest.mark.randomize(left=int, top=int, right=int, bottom=int, min_num=1,
                       max_num=MAX)
@pytest.mark.randomize(width=int, height=int, min_num=1, max_num=MAX)
def test_resize(width, height, left, top, right, bottom):
    # sort the percents
    top, bottom = sorted([top, bottom])
    left, right = sorted([left, right])

    left = get_percent(width, left)
    right = get_percent(width, right)
    top = get_percent(height, top)
    bottom = get_percent(height, bottom)

    # ignore 0 sized crops
    if left == right or top == bottom:
        return


    # identity proprety
    box = model.new_box(width, height, 0, 0, width, height)
    id_box = model.resize(box, width, height)
    assert id_box == box

    # identity property with a crop
    box = model.new_box(width, height, left, top, right, bottom)
    box_size = size(box)
    id_box = model.resize(box, box_size.width, box_size.height)
    assert id_box == box

    # inverse property
    box = model.new_box(width, height, left, top, right, bottom)
    box2 = model.resize(box, half(width), half(height))
    box2_size = size(box2)
    box2 = model.resize(box2,
                        double(box2_size.width),
                        double(box2_size.height),
    )

