module Fixture_new_variable_prime_suffix_Haskell where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
a' :: Val
a' = 1
main :: IO ()
main = seq a' (return ())
