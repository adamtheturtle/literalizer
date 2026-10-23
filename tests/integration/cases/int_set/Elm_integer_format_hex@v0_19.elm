module Check exposing (..)


type Val
    = EInt Int
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EInt 0x1,
    EInt 0x2,
    EInt 0x3
    ]
