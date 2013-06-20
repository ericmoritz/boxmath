import pytest
from boxmath import model
from boxmath.model import size
from fractions import Fraction

def get_percent(total, percent):
    return int(
        total * percent / 100.0
    )


@pytest.mark.randomize(left=int, top=int, right=int, bottom=int, min_num=1)
@pytest.mark.randomize(width=int, height=int, min_num=1)
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
    box2 = model.resize(box, width / 2, height / 2)
    box2_size = size(box2)
    box2 = model.resize(box2, 
                          box2_size.width * 2, 
                          box2_size.height * 2
                          )
    

@pytest.mark.randomize(orig_size=int, min_num=1)
@pytest.mark.randomize(req_size=int, min_num=1)
@pytest.mark.randomize(offset1=int, offset2=int, min_num=0, max_num=100)
def test_scale_dimension(orig_size, req_size, offset1, offset2):
    # the two offsets have to be < org_size so we made them a
    # percentage of org_size
    offset1, offset2 = sorted([offset1, offset2])
    offset1 = get_percent(orig_size, offset1)
    offset2 = get_percent(orig_size, offset2)

    # ignore offsets that are the same
    if offset1 == offset2:
        return None


    def invert((new_size, new_offset1, new_offset2)):
        crop_size = offset2 - offset1
        return model.scale_dimension(
            crop_size,
            new_size,
            new_offset1,
            new_offset2
            )

    # assert the inverse
    assert (orig_size, offset1, offset2) == invert(model.scale_dimension(
            req_size,
            orig_size,
            offset1,
            offset2
            ))

    # assert the identity property

    # If I ask for the crop size, I should get the orig_size back
    crop_size = offset2 - offset1
    (orig_size, offset1, offset2) = model.scale_dimension(
        crop_size, orig_size, offset1, offset2)

