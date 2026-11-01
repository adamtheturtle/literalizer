module Fixture_external_scalar_reference_Haskell_ref_default_existing_equation where
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
shared :: Val
shared = 1
my_data :: Val
my_data = shared
main :: IO ()
main = do
    _ <- consume_widget my_data
    pure ()
