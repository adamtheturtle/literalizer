module Fixture_yaml_plain_equals_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("x", HStr "=")
    -- unrelated
    ]
main :: IO ()
main = seq my_data (return ())
