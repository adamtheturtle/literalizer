module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 1,
    PStr "email",
    PStr "a@gmail.com",
    PInt 100
    ]
