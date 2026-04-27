module check where
data Val = HNull | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("host", HStr "localhost"),
    ("port", HNull)  -- not configured yet
    ]
