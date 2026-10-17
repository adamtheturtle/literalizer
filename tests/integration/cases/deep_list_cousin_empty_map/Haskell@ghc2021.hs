module Fixture_deep_list_cousin_empty_map_Haskell where
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
my_data = HList [
    HMap [("items", HList [HMap [("inner", HMap [("x", 1)])], HMap [("inner", HMap [])]])],
    HMap [("items", HList [HMap [("inner", HMap [("x", 2)])], HMap [("inner", HMap [])]])]
    ]
main :: IO ()
main = seq my_data (return ())
