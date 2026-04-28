module Fixture_string_with_hash_Haskell where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "issue #{42}",
    HStr "color #red"
    ]
