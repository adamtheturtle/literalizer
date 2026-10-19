module Check where


data Val
    = PInt Int
    | PFloat Number
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 1,
    PStr "a",
    PFloat 2.5
]
