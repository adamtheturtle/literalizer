module Fixture_dict_null_trailing_inline_comment_Haskell where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("host", HStr "localhost"),
    ("port", HNull)  -- not configured yet
    ]
main :: IO ()
main = seq my_data (return ())
