module Fixture_nested_array_maps_Haskell where
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
    ("groups", HList [HList [HMap [("id", 1)]], HList [HMap [("id", 2)]]])
    ]
main :: IO ()
main = seq my_data (return ())
