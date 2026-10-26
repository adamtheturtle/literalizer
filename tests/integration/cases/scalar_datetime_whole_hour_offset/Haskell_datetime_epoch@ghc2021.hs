module Fixture_scalar_datetime_whole_hour_offset_Haskell_datetime_epoch where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data :: Val
my_data = 1705323600
main :: IO ()
main = seq my_data (return ())
