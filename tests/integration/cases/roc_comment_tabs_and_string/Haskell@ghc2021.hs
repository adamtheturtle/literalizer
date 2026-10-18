module Fixture_roc_comment_tabs_and_string_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    -- before	line
    ("value", HStr "left\tright")  -- inline	line
    -- after	line
    ]
main :: IO ()
main = seq my_data (return ())
