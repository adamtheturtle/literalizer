module Fixture_literalize_ref_external_declaration_Haskell_ref_default where
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
shared :: Val
shared = HList [
    1,
    2
    ]
main :: IO ()
main = do
    _ <- my_data :: Val
    _ <- my_data = shared
    pure ()
