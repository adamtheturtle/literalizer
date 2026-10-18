module Fixture_cpp_variant_int32_boundaries_map_Haskell_integer_format_octal where
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
    ("below", -0o20000000001),
    ("minimum", -0o20000000000),
    ("above", -0o17777777777),
    ("nested", HList [0o0])
    ]
main :: IO ()
main = seq my_data (return ())
