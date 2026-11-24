module Fixture_call_target_identifier_length_64_Haskell_call where
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff :: Val -> IO ()
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff _ = return ()
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
    _ <- ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (1)
    pure ()
