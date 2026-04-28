module Fixture_int_list_with_zero_Haskell_integer_format_octal_zero where
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
    0o0,
    0o1,
    -0o1
    ]
main :: IO ()
main = seq my_data (return ())
