module Fixture_dict_dollar_ref_key_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("$ref", HStr "my_var")
    ]
main :: IO ()
main = seq my_data (return ())
