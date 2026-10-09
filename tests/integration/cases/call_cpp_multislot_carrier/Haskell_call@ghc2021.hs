module Fixture_call_cpp_multislot_carrier_Haskell_call where
process :: Val -> Val -> IO ()
process _ _ = return ()
data Val = HNull | HBool Bool | HInt Integer | HFloat Double | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate (HFloat f) = HFloat (negate f)
    negate _ = error "not implemented"
instance Fractional Val where
    fromRational r = HFloat (realToFrac r)
    _ / _ = error "not implemented"
main :: IO ()
main = do
    _ <- process (1) (HStr "hello")
    _ <- process (HStr "two") (HBool False)
    _ <- process (3.5) (HNull)
    pure ()
