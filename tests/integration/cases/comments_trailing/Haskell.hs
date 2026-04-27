module Fixture_comments_trailing_haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a"
    -- trailing
    ]
