module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 0,
    PInt 1,
    PInt (-1)
    ]
