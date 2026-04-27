module check where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    -- # section
    HStr "a"
    ]
