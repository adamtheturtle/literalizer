module Fixture_negative_nondecimal_i32_boundary_Haskell_integer_format_hex where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
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
    ("minimum", -0x80000000),
    ("below", -0xb2d05e00)
    ]
main :: IO ()
main = seq my_data (return ())
