module Fixture_null_only_ordered_map_Haskell_type_hints_safe where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("missing", HNull)
    ]
main :: IO ()
main = seq my_data (return ())
