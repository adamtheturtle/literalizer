module Check where


data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PStr "2000-01-01T01:02:03",
    PInt 1
]
