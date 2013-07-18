module Algorithm (new, crop, resize, apply) where

type Crop = (Float, Float, Float, Float)

data State = State {
  wscale :: Float,
  hscale :: Float,
  crop_ :: Crop
} deriving (Show)


new :: Float -> Float -> State
new w h = State 1.0 1.0 (0.0, 0.0, w, h)

crop :: Crop -> State -> State
crop crop0 s =
  s {crop_=scaleCrop crop0 (wscale s) (hscale s)}
  
scaleCrop :: Crop -> Float -> Float -> Crop
scaleCrop (l,t,r,b) ws hs =
     (l/ws, t/hs, r/ws, b/hs)

resize :: Float -> Float -> State -> State
resize w h s =
  s {wscale = ws, hscale=hs, crop_=crop'}
  where 
    (l,t,r,b) = crop_ s
    cw = r - l
    ch = b - t
    ws = w / cw
    hs = h / ch
    crop' = crop_ s

apply :: (Float -> Float -> a -> a) -> (Crop -> a -> a) -> State -> (a -> a)
apply resize_cb crop_cb s =
  resize_cb w' h' . crop_cb crop'
  where 
    (l,t,r,b) = crop_ s
    ws = wscale s
    hs = hscale s
    cw = r - l
    ch = b - t
    w' = cw * ws
    h' = ch * hs
    crop' = crop_ s

