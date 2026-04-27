module Check where


data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 1,
    PInt 2,
    PInt 3
    ]
