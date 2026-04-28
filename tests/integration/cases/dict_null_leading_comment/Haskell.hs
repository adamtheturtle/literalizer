module Fixture_dict_null_leading_comment_Haskell where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    -- comment
    ("name", HStr "Alice"),
    ("score", HNull)
    ]
