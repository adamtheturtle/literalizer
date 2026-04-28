module Fixture_call_per_element_false_Haskell_call where
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
main :: IO ()
main = do
    _ <- process(1)
    pure ()
