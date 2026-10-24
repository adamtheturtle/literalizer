module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 0x1,
    PStr "email",
    PStr "a@gmail.com",
    PInt 0x64
]
