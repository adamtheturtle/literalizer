module Fixture_literalize_ref_nested_null_Haskell_ref where
data Val = HNull | HList [Val]
myNull :: Val
myNull = HNull
my_data :: Val
my_data = HList [
    myNull,
    HNull
    ]
main :: IO ()
main = seq my_data (return ())
