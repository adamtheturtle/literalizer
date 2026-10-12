module Fixture_literalize_ref_v_null_Haskell_ref where
data Val = HNull
value :: Val
value = HNull
my_data :: Val
my_data = value
main :: IO ()
main = seq my_data (return ())
