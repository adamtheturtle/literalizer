module Check where


data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PInt 1, PInt 2],
    PList [],
    PList [PInt 3, PInt 4]
    ]
