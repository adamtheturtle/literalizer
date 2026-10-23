module Check where


data Val
    = PBool Boolean
    | PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 0x2a,
    PFloat 3.14,
    PBool true,
    PBool false,
    PStr "hello \"world\""
]
