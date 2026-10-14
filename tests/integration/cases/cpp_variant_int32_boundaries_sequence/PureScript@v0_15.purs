module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt ((-2147483647 - 1)),
    PInt (-2147483647),
    PList [PInt 0]
]
