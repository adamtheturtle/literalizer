module Fixture_call_dispatch_Haskell_call where
put :: Val -> Val -> IO ()
put _ _ = return ()
get :: Val -> IO ()
get _ = return ()
data Val = HInt Integer | HList [Val]
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
    _ <- put (1) (10)
    _ <- get (1)
    pure ()
