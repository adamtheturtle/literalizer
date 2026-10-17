module Fixture_d_subnormal_floats_Haskell where
data Val = HFloat Double | HList [Val]
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
my_data = HList [
    5.0e-324,
    -5.0e-324,
    1.0e-310
    ]
main :: IO ()
main = seq my_data (return ())
