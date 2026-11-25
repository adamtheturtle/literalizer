module Fixture_jsonc_comment_nested_empty_dicts_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    -- outer heading
    -- first empty
    ("a", HMap []),
    -- second empty
    ("b", HMap [])
    ]
main :: IO ()
main = seq my_data (return ())
