module Fixture_systemverilog_keyword_prefix_variable_Haskell where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
first_value :: Val
first_value = 1
main :: IO ()
main = seq first_value (return ())
