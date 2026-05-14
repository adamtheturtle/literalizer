module Fixture_scalar_bool_Haskell where
data Val = HBool Bool
my_data :: Val
my_data = HBool True
main :: IO ()
main = seq my_data (return ())
