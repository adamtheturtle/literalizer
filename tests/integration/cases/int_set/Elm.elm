module Check exposing (..)


type Val
    = EInt Int
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EInt 1,
    EInt 2,
    EInt 3
    ]
