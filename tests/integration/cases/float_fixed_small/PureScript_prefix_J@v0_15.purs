module Check where


import Prelude
data Val
    = JFloat Number
    | JList (Array Val)


my_data :: Val
my_data = JList [
    JFloat 1.0e-9,
    JFloat (-1.0e-9)
]
