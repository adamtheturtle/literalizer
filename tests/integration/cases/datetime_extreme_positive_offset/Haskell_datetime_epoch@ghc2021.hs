module Fixture_datetime_extreme_positive_offset_Haskell_datetime_epoch where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data :: Val
my_data = 1592136060
main :: IO ()
main = seq my_data (return ())
