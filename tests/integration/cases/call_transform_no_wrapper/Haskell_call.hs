module Fixture_call_transform_no_wrapper_Haskell_call where
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> IO Val
process _ = return undefined
main :: IO ()
main = do
    _ <- process(HStr "hello")
    _ <- process(42)
    _ <- process(HBool True)
    pure ()
