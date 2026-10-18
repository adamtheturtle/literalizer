module Check where


import Prelude
data Val
    = PInt Int
    | PLong Number
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PLong (-2147483649.0),
    PInt ((-2147483647 - 1)),
    PInt 2147483647,
    PLong 2147483648.0
]
