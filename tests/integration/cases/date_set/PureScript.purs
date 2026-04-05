module Check where


data Val
    = PStr String
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PStr "2024-01-15",
    PStr "2024-06-01"
    ]
