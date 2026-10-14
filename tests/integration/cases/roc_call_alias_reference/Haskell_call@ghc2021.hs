module Fixture_roc_call_alias_reference_Haskell_call where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
process :: Val -> IO ()
process _ = return ()
value :: Val
value = 1
main :: IO ()
main = do
    _ <- process value
    pure ()
