module Fixture_call_scalar_args_Haskell_call where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> IO ()
process _ = return ()
main :: IO ()
main = do
    _ <- process(HStr "hello")
    _ <- process(42)
    _ <- process(HBool True)
    pure ()
