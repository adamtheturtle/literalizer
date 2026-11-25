module Fixture_bom_in_string_value_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("v", HStr "a\xfeff\&b")
    ]
main :: IO ()
main = seq my_data (return ())
