module Check where
data JsonVal = HStr String | HList [JsonVal]
my_data :: JsonVal
my_data = HList [
    HStr "48656c6c6f"
    ]
