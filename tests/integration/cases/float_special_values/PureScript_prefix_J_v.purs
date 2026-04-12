module Check where


import Prelude
data Val
    = JFloat Number
    | JList (Array Val)


my_data :: Val
my_data = JList [
    JFloat (1.0 / 0.0),
    JFloat (-(1.0 / 0.0)),
    JFloat (0.0 / 0.0)
    ]
