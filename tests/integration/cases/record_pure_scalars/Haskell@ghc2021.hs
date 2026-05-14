module Fixture_record_pure_scalars_Haskell where
data Val = HBool Bool | HInt Integer | HFloat Double | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("name", HStr "Alice"),
    ("age", 30),
    ("active", HBool True),
    ("score", 4.5)
    ]
main :: IO ()
main = seq my_data (return ())
