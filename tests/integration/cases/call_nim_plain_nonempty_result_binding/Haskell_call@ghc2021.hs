{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_nim_plain_nonempty_result_binding_Haskell_call where
make_widget :: Val -> IO Val
make_widget _ = return undefined
data Val = HInt Integer | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data = make_widget (HList [1])
main :: IO ()
main = seq my_data (return ())
