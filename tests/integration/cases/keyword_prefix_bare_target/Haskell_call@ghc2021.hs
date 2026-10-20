module Fixture_keyword_prefix_bare_target_Haskell_call where
first_value :: Val -> IO ()
first_value _ = return ()
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
main :: IO ()
main = do
    _ <- first_value (1)
    pure ()
