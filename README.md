===================================================================
boxmath
===================================================================

This provides image crop/resize monanoid for chaining multiple resize,
crop actions and producing a resulting crop/resize action pair.

This is possible given the following insights:

    box resize (width, height) resize (w2, h2) = box resize (w2, h2)
    box crop (left, top, right, bottom) crop (l,t,r,b) = box crop (left+l, top+t, left+r, top+b)

With these two insights, we can compose two resize and two crop
actions.  The next step is composing a resize and crop action.

This is possible using a ResizeCrop Monoid whose dot function keeps
track of the resize width, height and crop box and scales these values
appropriately:

```haskell
    Crop l t r b . Crop l t r b -> Crop l t r b
    Crop l1 t1 r1 b1 . Crop l2 t2 r2 b2 = Crop l1+l2 t1+t2 l1+r2 t1+b2

    (ResizeCrop r c) scale (Resize w h) -> ResizeCrop r c

    ResizeCrop r c . ResizeCrop r c -> ResizeCrop r c
    ResizeCrop r1 c1 . ResizeCrop r2 c2 = do 
        r3, c3 = ResizeCrop r1 c1) scale r2
        ResizeCrop r3 (c3 . c2)
```

(I appologize for the terrible pseudo-Haskell)
