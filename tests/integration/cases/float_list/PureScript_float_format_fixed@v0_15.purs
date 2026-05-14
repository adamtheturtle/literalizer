module Check where


import Prelude
data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PFloat 1.100000,
    PFloat (-2.200000),
    PFloat 3.300000
    ]
