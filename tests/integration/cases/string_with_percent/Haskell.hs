module check where
data Val = HStr String | HList [Val]
my_data :: Val
my_data = HList [
    HStr "100% done",
    HStr "%(name) is here"
    ]
