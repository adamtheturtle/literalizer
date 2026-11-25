module Check where


import Prelude
data Val
    = PFloat Number
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PFloat 5.0e-324,
    PFloat (-5.0e-324),
    PFloat 2.2250738585072014e-308
]
