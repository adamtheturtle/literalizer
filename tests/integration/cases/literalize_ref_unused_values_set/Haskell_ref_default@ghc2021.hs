module Fixture_literalize_ref_unused_values_set_Haskell_ref_default where
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
    2
    ]
main :: IO ()
main = seq my_data (return ())
