module Check where


import Prelude
data Val
    = PInt Int
    | PLong Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PLong 999999999999999999.0,
    PLong (-999999999999999999.0)
    ]
