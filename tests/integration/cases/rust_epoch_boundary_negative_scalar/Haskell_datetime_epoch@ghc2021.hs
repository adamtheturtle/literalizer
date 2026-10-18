module Fixture_rust_epoch_boundary_negative_scalar_Haskell_datetime_epoch where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data :: Val
my_data = -2147483649
main :: IO ()
main = seq my_data (return ())
