module Fixture_dict_with_homogeneous_annotated_values_Haskell_collection_layout_multiline where
data Val = HStr String | HList [Val] | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("a", HList []),
    ("b", HList [])
    ]
main :: IO ()
main = seq my_data (return ())
