module Check where


data Val
    = PInt Int
    | PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PList [PInt 1],
    PList [PFloat 2.5]
]
