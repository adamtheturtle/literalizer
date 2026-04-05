module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PList [PInt 1, PInt 2], PList [PStr "a", PStr "b"]]
    ]
