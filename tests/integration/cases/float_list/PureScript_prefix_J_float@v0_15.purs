module Check where


import Prelude
data Val
    = JFloat Number
    | JList (Array Val)


my_data :: Val
my_data = JList [
    JFloat 1.1,
    JFloat (-2.2),
    JFloat 3.3
    ]
