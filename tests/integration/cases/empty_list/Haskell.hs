module Fixture_empty_list_Haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList []
main :: IO ()
main = seq my_data (return ())
