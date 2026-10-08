module Fixture_csharp_array_map_element_type_Haskell where
data Val = HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("d", HList [HMap [("a", HList [HMap [("b", HList [1, HList [2.5, HList [HStr "x", HList [HBool True]]]])]])]])
    ]
main :: IO ()
main = seq my_data (return ())
