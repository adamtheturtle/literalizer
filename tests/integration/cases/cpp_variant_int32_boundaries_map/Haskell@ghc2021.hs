module Fixture_cpp_variant_int32_boundaries_map_Haskell where
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
    ("below", -2147483649),
    ("minimum", -2147483648),
    ("above", -2147483647),
    ("nested", HList [0])
    ]
main :: IO ()
main = seq my_data (return ())
