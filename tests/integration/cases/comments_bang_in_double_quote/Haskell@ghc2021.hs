module Fixture_comments_bang_in_double_quote_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("key", HStr "\"bang!\"")  -- real
    ]
main :: IO ()
main = seq my_data (return ())
