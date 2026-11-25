module Check where


import Prelude
data Val
    = PInt Int
    | PLong Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PLong (-2147483649.0),
    PInt ((-2147483647 - 1)),
    PInt 2147483647,
    PLong 2147483648.0
]
