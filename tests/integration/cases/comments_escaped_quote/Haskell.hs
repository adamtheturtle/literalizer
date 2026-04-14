module Check where
data Val = HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("key", HStr "value \" # not a comment")  -- real
    ]
