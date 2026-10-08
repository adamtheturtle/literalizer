module Fixture_call_object_proto_parameter_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
capture :: Val -> IO ()
capture _ = return ()
main :: IO ()
main = do
    _ <- capture (1)
    pure ()
