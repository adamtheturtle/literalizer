module Fixture_datetime_epoch_far_future_Haskell_datetime_epoch_far_future where
data Val = HStr String | HMap [(String, Val)] | HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("ts", 32535215999)
    ]
main :: IO ()
main = seq my_data (return ())
