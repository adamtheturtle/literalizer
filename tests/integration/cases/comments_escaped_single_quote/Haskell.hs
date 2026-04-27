module check where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("key", HStr "it's here")  -- a comment
    ]
