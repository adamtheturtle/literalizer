module Fixture_dict_all_null_trailing_comment_Haskell where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("a", HNull),
    ("b", HNull)
    -- trailing
    ]
main :: IO ()
main = seq my_data (return ())
