module Fixture_literalize_ref_explicit_precedence_Haskell_ref where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
x :: Val
x = HList [
    1,
    2
    ]
my_data :: Val
my_data = x
main :: IO ()
main = seq my_data (return ())
