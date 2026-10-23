module Check where


data Val
    = PInt Int
    | PLong Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 0x1,
    PLong 1099511627776.0
]
