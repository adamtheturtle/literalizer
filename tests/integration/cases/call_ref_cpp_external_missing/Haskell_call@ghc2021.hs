module Fixture_call_ref_cpp_external_missing_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
consume :: Val -> IO ()
consume _ = return ()
item :: Val
item = HList [
    1,
    2
    ]
main :: IO ()
main = do
    _ <- consume item
    pure ()
