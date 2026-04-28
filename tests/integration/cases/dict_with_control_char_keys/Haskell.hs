module Fixture_dict_with_control_char_keys_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("key\nwith\nnewlines", HStr "value1"),
    ("key\twith\ttabs", HStr "value2"),
    ("", HStr "value3")
    ]
main :: IO ()
main = seq my_data (return ())
