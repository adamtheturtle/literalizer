module Fixture_call_bound_literal_followup_new_Haskell_call where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
make_widget :: Val -> IO Val
make_widget _ = return undefined
consume :: Val -> IO ()
consume _ = return ()
my_data = make_widget (42)
main :: IO ()
main = do
    _ <- consume my_data
    pure ()
