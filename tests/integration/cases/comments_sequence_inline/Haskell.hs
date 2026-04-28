module Fixture_comments_sequence_inline_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a",  -- note a
    HStr "b"  -- note b
    ]
