module Fixture_nested_deep_empty_Haskell where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [HList [], HList []]
    ]
main :: IO ()
main = seq my_data (return ())
