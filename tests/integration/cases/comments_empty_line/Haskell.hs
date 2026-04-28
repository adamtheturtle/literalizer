module Fixture_comments_empty_line_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a",
    --
    HStr "b"
    ]
