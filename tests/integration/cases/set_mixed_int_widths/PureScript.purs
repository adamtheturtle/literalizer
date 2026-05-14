module Check where


data Val
    = PInt Int
    | PLong Number
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PInt 1,
    PLong 1099511627776.0
    ]
