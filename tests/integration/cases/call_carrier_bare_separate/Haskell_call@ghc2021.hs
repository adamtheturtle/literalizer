module Fixture_call_carrier_bare_separate_Haskell_call where
make_widget :: Val -> Val -> IO ()
make_widget _ _ = return ()
data Val = HInt Integer | HStr String | HList [Val]
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
    _ <- make_widget (HList [1]) (HList [HStr "text"])
    pure ()
