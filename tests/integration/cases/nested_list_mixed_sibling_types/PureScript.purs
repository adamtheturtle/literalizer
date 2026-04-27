module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PInt 1, PInt 2],
    PList [],
    PList [PStr "a", PStr "b"]
    ]
