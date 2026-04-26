module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EList [EInt 1, EInt 2]],
    EList [],
    EList [EList [EInt 3, EInt 4]]
    ]
