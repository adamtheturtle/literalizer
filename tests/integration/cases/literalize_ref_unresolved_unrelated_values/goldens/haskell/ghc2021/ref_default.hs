module Fixture_literalize_ref_unresolved_unrelated_values_Haskell_ref_default where
data Val = HInt Integer | HList [Val]
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
a :: Val
a = 0
my_data :: Val
my_data = HList [
    a,
    1
    ]
main :: IO ()
main = do
    _ <- consume_widget my_data
    pure ()
