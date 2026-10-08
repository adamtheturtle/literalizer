module Check where


data Val
    = PInt Int
    | PList (Array Val)


x :: Val
x = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = x
