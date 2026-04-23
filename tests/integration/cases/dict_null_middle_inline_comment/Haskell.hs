module Check where
data Val = HNull | HBool Bool | HStr String | HMap [(String, Val)]
my_data :: Val
my_data = HMap [
    ("host", HStr "localhost"),
    ("port", HNull),  -- not configured yet
    ("debug", HBool True)
    ]
