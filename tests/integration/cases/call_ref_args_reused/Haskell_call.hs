module Fixture_call_ref_args_reused_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: (Val, Val) -> IO ()
process _ = return ()
single_var :: Val
single_var = HList [
    4,
    5,
    6
    ]
repeated_var :: Val
repeated_var = 1
main :: IO ()
main = do
    _ <- process(repeated_var, 1)
    _ <- process(single_var, 0)
    _ <- process(repeated_var, 8)
    pure ()
