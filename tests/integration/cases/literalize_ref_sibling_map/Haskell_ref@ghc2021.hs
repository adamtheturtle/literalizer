module Fixture_literalize_ref_sibling_map_Haskell_ref where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
siblingMap :: Val
siblingMap = HMap [
    ("k", 2)
    ]
my_data :: Val
my_data = HList [
    HMap [("k", 1)],
    siblingMap
    ]
main :: IO ()
main = seq my_data (return ())
