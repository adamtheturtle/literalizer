module Fixture_call_shared_wrapper_target_collision_Haskell_call where
check :: Val -> IO ()
check _ = return ()
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
    _ <- check (42)
    pure ()
