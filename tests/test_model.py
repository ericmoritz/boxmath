import pytest
from boxmath import model
from boxmath.model import size
from fractions import Fraction

def get_percent(total, percent):
    return int(
        total * percent / 100.0
    )


def half(num):
    return Fraction(num, 2)


def double(num):
    return num * 2


MAX=1000000

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

