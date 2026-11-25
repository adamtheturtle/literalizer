module Fixture_pre_indented_tagged_list_argument_Haskell_ref_default where
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
main :: IO ()
main = do
    _ <- consume_widget (    HList [
            1,
            2
            ])
    pure ()
