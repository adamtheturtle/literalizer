module Fixture_dict_with_quoted_digit_keys_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("0a", HStr "first"),
    ("1b", HStr "second")
    ]
main :: IO ()
main = seq my_data (return ())
