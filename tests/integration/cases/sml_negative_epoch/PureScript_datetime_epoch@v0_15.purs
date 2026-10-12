module Check where


import Prelude
data Val
    = PInt Int
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt (-315619200)
]
