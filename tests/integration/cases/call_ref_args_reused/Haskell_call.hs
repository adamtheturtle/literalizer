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
shared :: Val
shared = 1
other :: Val
other = 2
main :: IO ()
main = do
    _ <- process(shared, 1)
    _ <- process(other, 0)
    _ <- process(shared, 8)
    pure ()
