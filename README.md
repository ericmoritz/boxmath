===================================================================
boxmath
===================================================================

This provides image crop/resize monanoid for chaining multiple resize,
crop actions and producing a resulting crop/resize action pair.

This is possible given the following insights:

   box resize (width, height) resize (w2, h2) = box resize (w2, h2)
   box crop (left, top, right, bottom) crop (l,t,r,b) = box crop (left+l, top+t, left+r, top+b)

With these two insights, we can compose two resize and two crop actions.  The next step
is composing a resize and crop action.

This is possible using a ResizeCrop Monoid whose dot function keeps track of the resize width, height
and crop box and scales these values appropriately:

    ResizeCrop (Resize w1 h1) (Crop l1 t1 r1 b1) . ResizeCrop (Resize w2 h2) (Crop l2 t2 r2 b2) -> ResizeCrop (Resize w3 h3) (Crop l3 t3 r3 b3)

        

