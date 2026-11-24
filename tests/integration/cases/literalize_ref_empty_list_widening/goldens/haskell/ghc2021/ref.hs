module Fixture_literalize_ref_empty_list_widening_Haskell_ref where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
emptyValues :: Val
emptyValues = HList []
integerValues :: Val
integerValues = HList [
    1
    ]
my_data :: Val
my_data = HList [
    emptyValues,
    integerValues
    ]
main :: IO ()
main = seq my_data (return ())
