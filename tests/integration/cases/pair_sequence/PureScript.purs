module Check where


import Prelude
data Val
    = PInt Int
    | PStr String
    | PList (Array Val)


my_data :: Val
my_data = PList [
    PInt 1,
    PStr "hello"
    ]
