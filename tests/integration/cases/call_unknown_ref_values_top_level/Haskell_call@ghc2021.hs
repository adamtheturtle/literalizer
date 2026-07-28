module Fixture_call_unknown_ref_values_top_level_Haskell_call where
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
known_value :: Val
known_value = 1
unknown_value :: Val
unknown_value = HList []
main :: IO ()
main = do
    _ <- process unknown_value
    pure ()
