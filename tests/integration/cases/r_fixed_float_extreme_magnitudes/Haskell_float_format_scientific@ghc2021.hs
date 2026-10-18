module Fixture_r_fixed_float_extreme_magnitudes_Haskell_float_format_scientific where
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
    2.2250738585072014e-308,
    1.0e-307,
    1.0e21,
    -1.5e300,
    1.7976931348623157e308,
    -1.7976931348623157e308
    ]
main :: IO ()
main = seq my_data (return ())
