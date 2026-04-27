module Check where


data JsonVal
    = PStr String
    | PList (Array JsonVal)


my_data :: JsonVal
my_data = PList [
    PStr "48656c6c6f"
    ]
