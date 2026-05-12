module Fixture_int_set_Haskell_type_hints_safe_dt_haskell where
data Val = HInt Integer | HSet [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data :: Val
my_data = HSet [
    1,
    2,
    3
    ]
main :: IO ()
main = seq my_data (return ())
