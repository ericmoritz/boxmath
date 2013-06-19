from collections import namedtuple

Box = namedtuple("Box", ['width', 'height', 'left', 'top', 'right', 'bottom'])

def box(width, height):
    return Box(
        width, height, 0, 0, width, height
    )


def bbox(_box):
    return box(
        _box.right - _box.left,
        _box.bottom - _box.top
        )


def resize(box, width, height):
    """
    >>> resize(
    ...    Box(100, 100, 0, 0, 50, 50), # resulting image is 50x50
    ...    50, 50
    ... )
    Box(width=100.0, height=100.0, left=0.0, top=0.0, right=50.0, bottom=50.0)

    Takes a 0,0,100,100 crop of a 200x200 image.
    which results in a 100x100 and resizes it to 50x50
    
    This should scale everything by 1/2

    >>> resize(
    ...    Box(200, 200, 0, 0, 100, 100),
    ...    50, 50
    ... )
    Box(width=100.0, height=100.0, left=0.0, top=0.0, right=50.0, bottom=50.0)

    >>> resize(
    ...    Box(200, 200, 0, 0, 100, 100),
    ...    200, 200
    ... )
    Box(width=400.0, height=400.0, left=0.0, top=0.0, right=200.0, bottom=200.0)


    """
    box_bbox = bbox(box)
    width_scale = float(width) / float(box_bbox.width)
    height_scale = float(height) / float(box_bbox.height)

    return Box(
        box.width * width_scale,
        box.height * height_scale,
        box.left * width_scale,
        box.top * height_scale,
        box.right * width_scale,
        box.bottom * height_scale
    )


def crop(box, left, top, right, bottom):
    """
    >>> crop(
    ...     Box(320, 200, 10, 20, 30, 40),
    ...     0, 0, 15, 25
    ... )
    Box(width=320, height=200, left=10, top=20, right=25, bottom=45)
    """
    return Box(
        box.width,
        box.height,
        box.left + left,
        box.top + top,
        box.left + right,
        box.top + bottom,
   )
    

def make_transformer(box, resize_cb, crop_cb):
    def inner(img0):
        img1 = resize_cb(img0, box.width, box.height)
        return crop_cb(img1, box.left, box.top, box.right, box.bottom)
    return inner

