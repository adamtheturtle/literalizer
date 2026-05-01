module Check where


data Val
    = PInt Int
    | PList (Array Val)
    | PSet (Array Val)


my_data :: Val
my_data = PList [
    PSet [],
    PSet [PInt 1, PInt 2],
    PList []
    ]
