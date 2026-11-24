module Fixture_scalar_datetime_non_utc_Haskell_datetime_epoch_non_utc where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data :: Val
my_data = 1705321800
main :: IO ()
main = seq my_data (return ())
