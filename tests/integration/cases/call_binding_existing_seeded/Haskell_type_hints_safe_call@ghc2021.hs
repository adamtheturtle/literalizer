module Fixture_call_binding_existing_seeded_Haskell_type_hints_safe_call where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
make_widget :: Val -> IO Val
make_widget _ = return undefined
my_data = make_widget (42)
my_data = make_widget my_data
main :: IO ()
main = do
    _ <- make_widget my_data
    pure ()
