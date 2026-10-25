module Fixture_dict_string_with_del_before_hex_letter_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("value", HStr "del\x7f\&d")
    ]
main :: IO ()
main = seq my_data (return ())
