module Check where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "a",  -- note a
    HStr "b"  -- note b
    ]
