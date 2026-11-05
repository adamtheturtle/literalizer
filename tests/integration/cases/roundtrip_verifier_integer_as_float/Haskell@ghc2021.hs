module Fixture_roundtrip_verifier_integer_as_float_Haskell where
data Val = HFloat Double | HStr String | HMap [(String, Val)]
instance Num Val where
    fromInteger n = HFloat (fromIntegral n)
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
my_data :: Val
my_data = HMap [
    ("value", 1.0)
    ]
main :: IO ()
main = seq my_data (return ())
