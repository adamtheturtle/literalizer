module Fixture_set_comments_Haskell where
data Val = HStr String | HSet [Val]
my_data :: Val
my_data = HSet [
    HStr "apple",  -- inline comment
    -- before banana
    HStr "banana"
    -- trailing
    ]
