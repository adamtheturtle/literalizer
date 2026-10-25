module Fixture_call_bound_scalar_declaration_variants_Haskell_call where
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
consume :: Val -> IO ()
consume _ = return ()
shared :: Val
shared = 42
main :: IO ()
main = do
    _ <- consume shared
    pure ()
