module check where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    -- line 1
    -- line 2
    HStr "a"
    ]
