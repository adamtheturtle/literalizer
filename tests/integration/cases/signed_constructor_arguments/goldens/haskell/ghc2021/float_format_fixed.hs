module Fixture_signed_constructor_arguments_Haskell_float_format_fixed where
data Val = HInt Integer | HFloat Double | HList [Val]
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
my_data = HList [
    -42,
    0,
    42,
    -1.250000,
    0.000000,
    1.250000
    ]
main :: IO ()
main = seq my_data (return ())
