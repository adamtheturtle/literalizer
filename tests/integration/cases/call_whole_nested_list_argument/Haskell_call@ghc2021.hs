module Fixture_call_whole_nested_list_argument_Haskell_call where
f :: Val -> IO ()
f _ = return ()
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
    _ <- f (HList [HList [1, 2], HList [3]])
    pure ()
