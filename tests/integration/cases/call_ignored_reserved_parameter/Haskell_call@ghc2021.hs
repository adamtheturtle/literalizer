module Fixture_call_ignored_reserved_parameter_Haskell_call where
process :: Val -> IO ()
process _ = return ()
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
main :: IO ()
main = do
    _ <- process (42)
    pure ()
