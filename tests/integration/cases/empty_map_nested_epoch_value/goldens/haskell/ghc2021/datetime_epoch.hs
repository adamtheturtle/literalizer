module Fixture_empty_map_nested_epoch_value_Haskell_datetime_epoch where
data Val = HStr String | HList [Val] | HMap [(String, Val)] | HInt Integer
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
    HMap [("nested", HMap [("times", HList [-2208988800])])],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
