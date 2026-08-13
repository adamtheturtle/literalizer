module Check where


data Val
    = PInt Int
    | PList (Array Val)


refX :: Val
refX = PInt 3
my_data :: Val
my_data = PList [
    refX,
    PInt 1,
    PInt 2
    ]
