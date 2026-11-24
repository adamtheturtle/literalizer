module Fixture_shared_invocation_single_integer_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
consume :: Val -> IO ()
consume _ = return ()
main :: IO ()
main = do
    _ <- consume (1)
    pure ()
