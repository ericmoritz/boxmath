module Main where

import qualified Algorithm as A
import qualified Model as M
import Test.QuickCheck
import Test.QuickCheck.Arbitrary

prop_crop_resize =
  forAll new_crop_resize property
  where
    property (w,h,crop,w1,h1) =
      cmp m a
      where
        m = M.resize w1 h1 $ M.crop crop $ M.new w h
        (w',h',crop') = A.apply $ A.resize w1 h1 $ A.crop crop $ A.new w h
        a = M.resize w' h' $ M.crop crop' $ M.new w h

prop_resize_crop =
  forAll new_resize_crop property
  where
    property (w,h,crop,w1,h1) =
      cmp m a
      where
        m = M.crop crop $ M.resize w1 h1 $ M.new w h
        (w',h',crop') = A.apply $ A.crop crop $ A.resize w1 h1 $ A.new w h
        a = M.resize w' h' $ M.crop crop' $ M.new w h

cmp (ml,mt,mr,mb) (al,at,ar,ab) =
  map floor m == map floor a
  where
    m = [ml,mt,mr,mb]
    a = [al,at,ar,ab]

new_crop_resize = do
  w <- arbitrary
  h <- arbitrary
  w1 <- arbitrary
  h1 <- arbitrary

  l <- choose (1, w)
  t <- choose (1, h)
  r <- choose (l, w)
  b <- choose (t, h)

  return (w,h,(l,t,r,b),w1,h1)

new_resize_crop = do
  w <- choose (1, 1000)
  h <- choose (1, 1000)
  w1 <- choose (1, 1000)
  h1 <- choose (1, 1000)

  l <- choose (1, w1)
  t <- choose (1, h1)
  r <- choose (l, w1)
  b <- choose (t, h1)


  return (w,h,(l,t,r,b),w1,h1)
  
main = quickCheck (prop_resize_crop .&&. prop_crop_resize)

