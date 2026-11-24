module Check where


data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [],
    PList [PInt 1],
    PList [PInt 1, PInt 2],
    PList [PInt 1, PStr "x", PBool true, PNull],
    PList [PInt 1, PInt 2, PInt 3, PInt 4, PInt 5, PInt 6, PInt 7, PInt 8]
]
