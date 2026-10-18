module Fixture_literalize_ref_bound_boolean_Haskell_ref where
data Val = HBool Bool
refFlag :: Val
refFlag = HBool True
my_data :: Val
my_data = refFlag
main :: IO ()
main = seq my_data (return ())
