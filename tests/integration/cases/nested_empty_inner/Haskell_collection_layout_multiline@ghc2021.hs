module Fixture_nested_empty_inner_Haskell_collection_layout_multiline where
data Val = HList [Val]
my_data :: Val
my_data = HList [
    HList [],
    HList []
    ]
main :: IO ()
main = seq my_data (return ())
