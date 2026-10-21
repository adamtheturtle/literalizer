module Fixture_ordered_map_string_values_Haskell_collection_layout_multiline where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("first", HStr "one"),
    ("second", HStr "two"),
    ("third", HStr "three")
    ]
main :: IO ()
main = seq my_data (return ())
