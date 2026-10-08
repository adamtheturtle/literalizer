module Fixture_epoch_datetime_map_values_Haskell_datetime_epoch where
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
    ("within_i32", 1705320000),
    ("beyond_i32", 4085195400)
    ]
main :: IO ()
main = seq my_data (return ())
