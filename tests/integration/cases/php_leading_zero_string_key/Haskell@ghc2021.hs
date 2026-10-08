module Fixture_php_leading_zero_string_key_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("08", HStr "value")
    ]
main :: IO ()
main = seq my_data (return ())
