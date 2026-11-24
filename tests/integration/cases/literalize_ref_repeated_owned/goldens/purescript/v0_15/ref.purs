module Check where


data Val
    = PInt Int
    | PList (Array Val)


shared :: Val
shared = PList [
    PInt 1,
    PInt 2
]
my_data :: Val
my_data = PList [
    shared,
    shared
]
