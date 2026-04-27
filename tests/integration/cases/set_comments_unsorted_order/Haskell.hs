module check where
data Val = HStr String | HSet [Val]
my_data :: Val
my_data = HSet [
    -- before apple
    HStr "apple",
    HStr "banana"  -- banana inline
    -- trailing
    ]
