module Fixture_set_mixed_int_widths_Haskell_integer_format_hex where
data Val = HInt Integer | HSet [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HSet [
    0x1,
    0x10000000000
    ]
main :: IO ()
main = seq my_data (return ())
