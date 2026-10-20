{-# OPTIONS_GHC -Wno-missing-signatures #-}
module Fixture_call_type_alias_bound_result_Haskell_call where
process :: Val -> IO Val
process _ = return undefined
data Val = HInt Integer
instance Num Val where
    fromInteger = HInt
    _ + _ = error "not implemented"
    _ * _ = error "not implemented"
    abs _ = error "not implemented"
    signum _ = error "not implemented"
    negate (HInt n) = HInt (negate n)
my_data = process (1)
main :: IO ()
main = seq my_data (return ())
