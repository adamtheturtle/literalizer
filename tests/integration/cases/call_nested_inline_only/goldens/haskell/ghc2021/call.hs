module Fixture_call_nested_inline_only_Haskell_call where
data Val = HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
f :: Val -> Val -> IO ()
f _ _ = return ()
main :: IO ()
main = do
    _ <- f (2) (HStr "hello")  -- trailing note
    _ <- f (3) (HStr "world")  -- another note
    pure ()
