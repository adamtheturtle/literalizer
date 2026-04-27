module Fixture_ordered_map_int_keys_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("1", HStr "one"),
    ("2", HStr "two"),
    ("42", HStr "answer")
    ]
