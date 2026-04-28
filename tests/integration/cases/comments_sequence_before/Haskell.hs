module Fixture_comments_sequence_before_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    -- first
    HStr "a",
    -- second
    HStr "b"
    ]
