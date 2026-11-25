module Check where


data Val
    = PInt Int
    | PList (Array Val)


whole :: Val
whole = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = whole
