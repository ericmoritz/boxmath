module Model (new, resize, crop) where
import Test.QuickCheck hiding (resize)
import Data.List (sort)
import Data.Ratio

type Crop a = (a, a, a, a)
type Size a = (a, a)

new w h = (0,0,w,h)

resize w h (l,t,r,b) =
    (l*ws, t*hs, r*ws, b*hs)
  where 
    w0 = r - l
    h0 = b - t
    ws = w / w0
    hs = h / h0


crop :: Crop Float -> Crop Float -> Crop Float
crop (l, t, r, b) (l0, t0, r0, b0) =
  (l0+l, t0+t, l0+r, t0+b)

