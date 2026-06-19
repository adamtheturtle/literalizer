module Fixture_call_dispatch_Haskell_call where
store_item :: Val -> Val -> IO ()
store_item _ _ = return ()
read_item :: Val -> IO ()
read_item _ = return ()
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
    _ <- store_item (1) (10)
    _ <- read_item (1)
    pure ()
