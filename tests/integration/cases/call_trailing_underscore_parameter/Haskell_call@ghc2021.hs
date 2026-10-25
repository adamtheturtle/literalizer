module Fixture_call_trailing_underscore_parameter_Haskell_call where
do_thing :: Val -> IO ()
do_thing _ = return ()
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
    _ <- do_thing (1)
    _ <- do_thing (2)
    pure ()
