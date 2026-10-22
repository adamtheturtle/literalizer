module Fixture_scalar_null_Haskell_type_hints_safe where
data Val = HNull
my_data :: Val
my_data = HNull
main :: IO ()
main = seq my_data (return ())
