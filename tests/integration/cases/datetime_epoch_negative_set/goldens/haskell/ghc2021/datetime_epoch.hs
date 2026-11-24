module Fixture_datetime_epoch_negative_set_Haskell_datetime_epoch where
data Val = HSet [Val] | HInt Integer
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
    -1
    ]
main :: IO ()
main = seq my_data (return ())
