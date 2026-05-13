module Fixture_literalize_ref_scalar_Haskell_ref where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
myInt :: Val
myInt = 42
my_data :: Val
my_data = myInt
main :: IO ()
main = seq my_data (return ())
