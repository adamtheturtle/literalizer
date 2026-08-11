module Check where


import Prelude
data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PFloat 0.000000001,
    PFloat (-0.000000001)
    ]
