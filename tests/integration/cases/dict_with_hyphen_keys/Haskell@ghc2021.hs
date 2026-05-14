module Fixture_dict_with_hyphen_keys_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("my-key", HStr "value1"),
    ("another-key", HStr "value2"),
    ("normal_key", HStr "value3")
    ]
main :: IO ()
main = seq my_data (return ())
