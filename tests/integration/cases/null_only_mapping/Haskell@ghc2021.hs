module Fixture_null_only_mapping_Haskell where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("value", HNull)
    ]
main :: IO ()
main = seq my_data (return ())
