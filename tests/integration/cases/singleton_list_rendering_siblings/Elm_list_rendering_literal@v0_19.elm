module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EInt 1],
    EList [],
    EList [EInt 2, EInt 3]
    ]
