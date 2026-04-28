module Fixture_ordered_map_nested_values_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("name", HStr "Alice"),
    ("scores", HMap [("1", HStr "first"), ("2", HStr "second")])
    ]
main :: IO ()
main = seq my_data (return ())
