module Check exposing (..)


type Val
    = EInt Int
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EInt 1,
    EInt 1099511627776
    ]
