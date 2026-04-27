module Check where


data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 0x1,
    PInt 0x2,
    PInt 0x3
    ]
