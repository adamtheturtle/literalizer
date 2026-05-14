module Fixture_int_list_large_Haskell_integer_format_binary_large where
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
    0b11110100001001000000,
    -0b10011010010,
    0b11111111,
    -0b1010
    ]
main :: IO ()
main = seq my_data (return ())
