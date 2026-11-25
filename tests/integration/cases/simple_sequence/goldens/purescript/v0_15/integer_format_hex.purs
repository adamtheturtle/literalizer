module Check where


data Val
    = PNull
    | PBool Boolean
    | PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 0x1,
    PStr "hello",
    PBool true,
    PNull
]
