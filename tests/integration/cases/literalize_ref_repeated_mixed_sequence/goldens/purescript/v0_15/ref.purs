module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


shared :: Val
shared = PList [
    PInt 1,
    PStr "x"
]
my_data :: Val
my_data = PList [
    shared,
    shared
]
