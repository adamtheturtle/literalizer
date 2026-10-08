module Fixture_cpp_mixed_sibling_maps_Haskell where
data Val = HNull | HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HList [
    HList [HMap [("a", 1)], HMap [("a", HNull)], 42],
    HList [HMap [("a", 1)], HMap [("a", HStr "s")], 42],
    HList [HMap [("a", 1)], HMap [("a", HNull)]],
    HList [HMap [("a", 1)], HMap [("a", HStr "s")]]
    ]
main :: IO ()
main = seq my_data (return ())
