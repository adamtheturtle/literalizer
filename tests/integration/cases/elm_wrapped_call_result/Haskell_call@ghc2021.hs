{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_elm_wrapped_call_result_Haskell_call where
make_widget :: Val -> IO Val
make_widget _ = return undefined
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data = make_widget (1)
main :: IO ()
main = seq my_data (return ())
