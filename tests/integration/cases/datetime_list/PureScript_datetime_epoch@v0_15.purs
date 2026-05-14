module Check where


data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 1705321800,
    PInt 1717228800
    ]
