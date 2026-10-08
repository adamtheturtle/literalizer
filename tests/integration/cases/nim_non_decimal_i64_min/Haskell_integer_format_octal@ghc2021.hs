module Fixture_nim_non_decimal_i64_min_Haskell_integer_format_octal where
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
    -0o1000000000000000000000,
    -0o1,
    0o777777777777777777777
    ]
main :: IO ()
main = seq my_data (return ())
