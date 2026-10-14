module Fixture_call_rust_epoch_boundary_Haskell_datetime_epoch_call where
consume :: Val -> IO ()
consume _ = return ()
data Val = HList [Val] | HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
main :: IO ()
main = do
    _ <- consume (-2147483649)
    _ <- consume (2147483648)
    pure ()
