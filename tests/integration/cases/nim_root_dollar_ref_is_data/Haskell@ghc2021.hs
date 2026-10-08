module Fixture_nim_root_dollar_ref_is_data_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("$ref", HStr "schema.json")
    ]
main :: IO ()
main = seq my_data (return ())
