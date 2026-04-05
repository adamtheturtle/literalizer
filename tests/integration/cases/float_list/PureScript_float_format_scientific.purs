module Check where


import Prelude
data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PFloat 1.1,
    PFloat (-2.2),
    PFloat 3.3
    ]
