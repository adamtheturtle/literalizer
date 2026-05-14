module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 1000000,
    PInt (-1234),
    PInt 255,
    PInt (-10)
    ]
