module Check where


data Val
    = PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "2024-01-15",
    PStr "2024-02-20"
    ]
