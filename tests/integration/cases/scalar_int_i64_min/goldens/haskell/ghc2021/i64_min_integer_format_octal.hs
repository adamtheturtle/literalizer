module Fixture_scalar_int_i64_min_Haskell_i64_min_integer_format_octal where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data :: Val
my_data = -0o1000000000000000000000
main :: IO ()
main = seq my_data (return ())
