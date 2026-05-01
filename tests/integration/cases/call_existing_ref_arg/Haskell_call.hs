module Fixture_call_existing_ref_arg_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
send :: Val -> IO ()
send _ = return ()
existing :: Val
existing = 42
main :: IO ()
main = do
    _ <- send(existing)
    pure ()
