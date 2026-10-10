module Check where


import Prelude
data Val
    = PInt Int
    | PSet (Array Val)


my_data :: Val
my_data = PSet [
    PInt (-1)
]
