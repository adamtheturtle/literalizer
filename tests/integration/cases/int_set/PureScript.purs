module Check where


data Val
    = PInt Int
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PInt 1,
    PInt 2,
    PInt 3
    ]
