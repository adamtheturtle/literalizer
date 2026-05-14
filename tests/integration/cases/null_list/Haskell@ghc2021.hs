module Fixture_null_list_Haskell where
data Val = HNull | HList [Val]
my_data :: Val
my_data = HList [
    HNull,
    HNull
    ]
main :: IO ()
main = seq my_data (return ())
