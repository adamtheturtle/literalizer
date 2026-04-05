module Check where


data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PBool true,
    PStr "hi",
    PList [PInt 1, PInt 2],
    PNull
    ]
