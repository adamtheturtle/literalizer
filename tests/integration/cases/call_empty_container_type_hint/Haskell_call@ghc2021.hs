module Fixture_call_empty_container_type_hint_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val] | HMap [(String, Val)]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
process :: Val -> Val -> IO ()
process _ _ = return ()
main :: IO ()
main = do
    _ <- process (HList [1, HMap []]) (42)
    pure ()
