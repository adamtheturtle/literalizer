module Fixture_literalize_ref_camel_name_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("$ref", HStr "myVar")
    ]
main :: IO ()
main = seq my_data (return ())
