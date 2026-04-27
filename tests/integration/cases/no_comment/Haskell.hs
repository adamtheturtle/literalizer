module Fixture_no_comment_haskell where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("message", HStr "no comment here")
    ]
