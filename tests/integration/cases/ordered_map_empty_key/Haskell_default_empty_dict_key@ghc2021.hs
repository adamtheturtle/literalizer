module Fixture_ordered_map_empty_key_Haskell_default_empty_dict_key where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("", HStr "unnamed"),
    ("named", HStr "value")
    ]
main :: IO ()
main = seq my_data (return ())
