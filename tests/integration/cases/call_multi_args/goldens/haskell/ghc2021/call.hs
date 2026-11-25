module Fixture_call_multi_args_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> Val -> IO ()
process _ _ = return ()
main :: IO ()
main = do
    _ <- process (1) (42)
    _ <- process (2) (100)
    pure ()
