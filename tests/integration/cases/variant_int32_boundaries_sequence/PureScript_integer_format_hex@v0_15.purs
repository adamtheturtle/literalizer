module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt ((-0x7fffffff - 0x1)),
    PInt (-0x7fffffff),
    PList [PInt 0x0]
]
