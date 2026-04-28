module Fixture_call_ref_args_converted_whole_Haskell_call where
data Val = HInt Integer | HList [Val]
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
myVar :: Val
myVar = HList [
    1,
    2,
    3
    ]
main :: IO ()
main = do
    _ <- process(myVar)
    pure ()
