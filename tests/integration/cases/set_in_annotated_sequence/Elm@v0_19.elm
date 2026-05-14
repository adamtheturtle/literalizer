module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
    | ESet (List Val)


my_data : Val
my_data = EList [
    ESet [],
    ESet [EInt 1, EInt 2],
    EList []
    ]
