module Fixture_scalar_int_very_large_Haskell_type_hints_safe where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data :: Val
my_data = 9223372036854775808
main :: IO ()
main = seq my_data (return ())
