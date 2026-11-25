module Fixture_literalize_ref_null_value_Haskell_ref where
data Val = HNull
myNull :: Val
myNull = HNull
my_data :: Val
my_data = myNull
main :: IO ()
main = seq my_data (return ())
