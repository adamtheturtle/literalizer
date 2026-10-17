module Fixture_jsonc_output_yaml_comments_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    -- server
    ("host", HStr "localhost")  -- default
    ]
main :: IO ()
main = seq my_data (return ())
