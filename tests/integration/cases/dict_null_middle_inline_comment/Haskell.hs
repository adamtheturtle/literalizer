module Fixture_dict_null_middle_inline_comment_Haskell where
data Val = HNull | HBool Bool | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("host", HStr "localhost"),
    ("port", HNull),  -- not configured yet
    ("debug", HBool True)
    ]
