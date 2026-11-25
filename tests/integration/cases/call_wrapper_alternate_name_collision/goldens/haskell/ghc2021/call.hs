module Fixture_call_wrapper_alternate_name_collision_Haskell_call where
check_wrapper :: Val -> IO ()
check_wrapper _ = return ()
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
    _ <- check_wrapper (42)
    pure ()
