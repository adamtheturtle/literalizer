module Check where


data Val
    = PStr String
    | PList (Array Val)
    | PSet (Array Val)


my_data :: Val
my_data = PList [
    PSet [PStr "a", PStr "b"]
    ]
