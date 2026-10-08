module Fixture_mojo_empty_filtered_ordered_map_Haskell where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("missing", HNull)
    ]
main :: IO ()
main = seq my_data (return ())
