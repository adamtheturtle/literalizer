module Fixture_float_scientific_notation_Haskell_float_format_scientific_s where
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
    0.0,
    1.0,
    1.5e3,
    1.0e-3,
    1.0e16
    ]
main :: IO ()
main = seq my_data (return ())
