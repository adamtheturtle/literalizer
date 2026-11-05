module Fixture_literalize_ref_unused_values_set_Haskell_ref_default_unwrapped_expression where
data Val = HInt Integer | HSet [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
consume_widget :: Val -> IO ()
consume_widget _ = return ()
main :: IO ()
main = do
    _ <- consume_widget (HSet [
        1,
        2
        ])
    pure ()
