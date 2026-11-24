module Fixture_comments_escaped_quote_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("key", HStr "value \" # not a comment")  -- real
    ]
main :: IO ()
main = seq my_data (return ())
