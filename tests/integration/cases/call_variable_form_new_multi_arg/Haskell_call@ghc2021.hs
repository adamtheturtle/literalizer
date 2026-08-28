{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_variable_form_new_multi_arg_Haskell_call where
record_entry :: Val -> Val -> Val -> IO Val
record_entry _ _ _ = return undefined
data Val = HBool Bool | HInt Integer | HStr String | HList [Val]
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
    negate _ = error "not implemented"
my_data = record_entry (HStr "a") (1) (HBool True)
main :: IO ()
main = seq my_data (return ())
