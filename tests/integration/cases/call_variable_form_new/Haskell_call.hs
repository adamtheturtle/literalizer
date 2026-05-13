module Fixture_call_variable_form_new_Haskell_call where
make_widget :: Val -> IO Val
make_widget _ = return undefined
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
result :: Val
result = make_widget (42)
main :: IO ()
main = seq result (return ())
