module Check where


data Val
    = PInt Int
    | PList (Array Val)


existing :: Val
existing = PInt 1
my_data :: Val
my_data = PList [
    PInt 0,
    PList [PList [existing]]
]
