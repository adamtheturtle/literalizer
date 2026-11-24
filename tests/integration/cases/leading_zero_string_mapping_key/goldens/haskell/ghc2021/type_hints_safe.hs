module Fixture_leading_zero_string_mapping_key_Haskell_type_hints_safe where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("08", HStr "value")
    ]
main :: IO ()
main = seq my_data (return ())
