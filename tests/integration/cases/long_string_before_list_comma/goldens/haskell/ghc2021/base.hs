module Fixture_long_string_before_list_comma_Haskell where
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HList [
    HStr "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    1
    ]
main :: IO ()
main = seq my_data (return ())
