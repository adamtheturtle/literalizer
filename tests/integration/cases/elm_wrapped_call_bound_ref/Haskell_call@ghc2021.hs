module Fixture_elm_wrapped_call_bound_ref_Haskell_call where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
make_widget :: Val -> IO ()
make_widget _ = return ()
value :: Val
value = 1
main :: IO ()
main = do
    _ <- make_widget value
    pure ()
