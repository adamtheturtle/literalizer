module Fixture_call_null_and_array_arguments_Haskell_call where
data Val = HNull | HInt Integer | HList [Val]
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
    _ <- process (HNull)
    _ <- process (HList [1, 2])
    pure ()
