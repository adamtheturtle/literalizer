module Fixture_empty_dicts_in_sequence_Haskell_collection_layout_multiline where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HList [
    HMap [],
    HMap []
    ]
main :: IO ()
main = seq my_data (return ())
