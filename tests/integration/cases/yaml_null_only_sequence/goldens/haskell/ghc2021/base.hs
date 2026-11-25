module Fixture_yaml_null_only_sequence_Haskell where
data Val = HNull | HList [Val]
my_data :: Val
my_data = HList [
    HNull
    ]
main :: IO ()
main = seq my_data (return ())
