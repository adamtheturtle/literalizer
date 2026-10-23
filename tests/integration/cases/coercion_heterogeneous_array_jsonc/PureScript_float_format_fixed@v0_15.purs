module Check where


data Val
    = PInt Int
    | PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 1,
    PFloat 2.500000,
    PInt 3
]
