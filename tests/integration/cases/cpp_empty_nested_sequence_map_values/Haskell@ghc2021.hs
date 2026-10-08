module Fixture_cpp_empty_nested_sequence_map_values_Haskell where
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
    ("alpha", HList [2, HList []]),
    ("beta", HList [5, HList [HStr "x"]])
    ]
main :: IO ()
main = seq my_data (return ())
