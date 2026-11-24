module Fixture_empty_set_Haskell where
data Val = HSet [Val]
my_data :: Val
my_data = HSet []
main :: IO ()
main = seq my_data (return ())
