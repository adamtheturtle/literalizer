module Fixture_dollar_ref_is_data_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("value", HMap [("$ref", HStr "foo")])
    ]
main :: IO ()
main = seq my_data (return ())
