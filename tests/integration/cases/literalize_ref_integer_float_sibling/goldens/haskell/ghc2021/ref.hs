module Fixture_literalize_ref_integer_float_sibling_Haskell_ref where
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
integerValue :: Val
integerValue = 1.0
my_data :: Val
my_data = HList [
    integerValue,
    1.5
    ]
main :: IO ()
main = seq my_data (return ())
