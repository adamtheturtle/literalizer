module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PInt 1, PStr "a"],
    PList [PInt 2, PStr "b"]
    ]
