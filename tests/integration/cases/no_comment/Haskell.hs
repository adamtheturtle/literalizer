module Fixture_no_comment_Haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("message", HStr "no comment here")
    ]
main :: IO ()
main = seq my_data (return ())
