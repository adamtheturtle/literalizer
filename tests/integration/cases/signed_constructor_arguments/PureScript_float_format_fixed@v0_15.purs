module Check where


import Prelude
data Val
    = PInt Int
    | PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt (-42),
    PInt 0,
    PInt 42,
    PFloat (-1.250000),
    PFloat 0.000000,
    PFloat 1.250000
]
