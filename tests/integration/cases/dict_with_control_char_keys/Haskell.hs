module check where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("key\nwith\nnewlines", HStr "value1"),
    ("key\twith\ttabs", HStr "value2"),
    ("", HStr "value3")
    ]
