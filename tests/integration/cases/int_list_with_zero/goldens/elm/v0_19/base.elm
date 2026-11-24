module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 0,
    EInt 1,
    EInt (-1)
    ]
