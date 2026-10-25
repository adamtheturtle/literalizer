module Fixture_special_float_std_binding_mapping_Haskell where
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
std :: Val
std = HMap [
    ("nan", HFloat ((0/0))),
    ("positive", HFloat ((1/0))),
    ("negative", HFloat ((-1/0)))
    ]
main :: IO ()
main = seq std (return ())
