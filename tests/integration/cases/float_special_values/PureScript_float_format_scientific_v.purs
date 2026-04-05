module Check where


import Prelude
data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PFloat (1.0 / 0.0),
    PFloat (-(1.0 / 0.0)),
    PFloat (0.0 / 0.0)
    ]
