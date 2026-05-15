module Fixture_record_wide_int_Haskell where
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
    ("quantity", 1000000),
    ("big", 18446744073709551615),
    ("ratio", 2.5),
    ("label", HStr "tag"),
    ("ok", HBool True)
    ]
main :: IO ()
main = seq my_data (return ())
