module Algorithm0 (new, resize, crop, apply) where

type Crop = (Float, Float, Float, Float)

data State = State {
  width :: Float,
  height :: Float,
  crop_ :: Crop
  }

new :: Float -> Float -> State
new w h = State w h (0,0,w,h)

resize :: Float -> Float -> State -> State
resize w h s =
  s {width=w', height=h', crop_=crop'}
  where
    (l,t,r,b) = (crop_ s)
    (w', l', r') = scaleDim w (width s) l r
    (h', t', b') = scaleDim h (height s) t b
    crop' = (l',t',r',b')

crop :: Crop -> State -> State
crop (l,t,r,b) s =
  s {crop_=crop'}
  where
    (l0,t0,_,_) = crop_ s
    crop' = (l',t',r',b')
    l' = l0 + l
    t' = t0 + t
    r' = l0 + r
    b' = t0 + b


apply :: (Float -> Float -> a -> a) -> (Crop -> a -> a) -> State -> (a -> a)
apply resize_cb crop_cb s =
  crop_cb c . resize_cb w h
  where
    w = (width s)
    h = (height s)
    c = (crop_ s)
  

scaleDim :: Float -> Float -> Float -> Float -> (Float, Float, Float)
scaleDim size1 size0 lower upper =
  (s', l', u')
  where
    span_ = upper - lower
    scale = size1 / span_
    s' = size0 * scale
    l' = lower * scale
    u' = upper * scale
    
