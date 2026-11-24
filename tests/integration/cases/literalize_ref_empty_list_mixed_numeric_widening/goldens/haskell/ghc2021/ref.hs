module Fixture_literalize_ref_empty_list_mixed_numeric_widening_Haskell_ref where
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
emptyValues :: Val
emptyValues = HList []
integerValues :: Val
integerValues = HList [
    1
    ]
floatValues :: Val
floatValues = HList [
    1.5
    ]
my_data :: Val
my_data = HList [
    emptyValues,
    integerValues,
    floatValues
    ]
main :: IO ()
main = seq my_data (return ())
