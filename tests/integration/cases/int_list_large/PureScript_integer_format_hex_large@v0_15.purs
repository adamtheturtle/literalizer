module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 0xf4240,
    PInt (-0x4d2),
    PInt 0xff,
    PInt (-0xa)
    ]
