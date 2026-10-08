module Fixture_raku_single_element_containers_Haskell where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("single_map", HList [HMap []]),
    ("single_list", HList [HList [1]]),
    ("single_deep", HList [HList [HList [2]]])
    ]
main :: IO ()
main = seq my_data (return ())
