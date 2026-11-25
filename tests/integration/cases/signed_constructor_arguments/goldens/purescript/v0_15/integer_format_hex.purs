module Check where


import Prelude
data Val
    = PInt Int
    | PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt (-0x2a),
    PInt 0x0,
    PInt 0x2a,
    PFloat (-1.25),
    PFloat 0.0,
    PFloat 1.25
]
