module check where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("name", HStr "Alice"),
    ("scores", HMap [("1", HStr "first"), ("2", HStr "second")])
    ]
