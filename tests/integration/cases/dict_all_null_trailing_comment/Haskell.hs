module Check where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("a", HNull),
    ("b", HNull)
    -- trailing
    ]
