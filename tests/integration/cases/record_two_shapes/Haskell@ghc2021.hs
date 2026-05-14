module Fixture_record_two_shapes_Haskell where
data Val = HInt Integer | HStr String | HMap [(String, Val)]
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
    ("metrics", HMap [("count", 100), ("rate", 50)]),
    ("flags", HMap [("retries", 3), ("timeout", 30)])
    ]
main :: IO ()
main = seq my_data (return ())
