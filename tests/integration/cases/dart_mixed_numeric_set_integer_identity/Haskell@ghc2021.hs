module Fixture_dart_mixed_numeric_set_integer_identity_Haskell where
data Val = HInt Integer | HFloat Double | HSet [Val]
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
my_data = HSet [
    1.5,
    9007199254740993
    ]
main :: IO ()
main = seq my_data (return ())
