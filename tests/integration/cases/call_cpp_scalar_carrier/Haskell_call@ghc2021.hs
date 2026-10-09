module Fixture_call_cpp_scalar_carrier_Haskell_call where
process :: Val -> IO ()
process _ = return ()
data Val = HNull | HBool Bool | HInt Integer | HStr String | HList [Val]
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
    _ <- process (HStr "hello")
    _ <- process (42)
    _ <- process (HBool True)
    _ <- process (HNull)
    pure ()
