module Fixture_int_list_signed_18_digit_boundaries_Haskell_integer_format_hex where
data Val = HInt Integer | HList [Val]
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
    0xde0b6b3a763ffff,
    -0xde0b6b3a763ffff
    ]
main :: IO ()
main = seq my_data (return ())
