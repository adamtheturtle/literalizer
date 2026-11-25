module Fixture_integer_type_name_variable_Haskell where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
i12345 :: Val
i12345 = 1
main :: IO ()
main = seq i12345 (return ())
