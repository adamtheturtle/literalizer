module Fixture_call_ref_args_Haskell_call where
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
my_var :: Val
my_var = HList [
    1,
    2,
    3
    ]
my_other :: Val
my_other = HList [
    4,
    5,
    6
    ]
main :: IO ()
main = do
    _ <- process(my_var, 42)
    _ <- process(my_other, 7)
    pure ()
