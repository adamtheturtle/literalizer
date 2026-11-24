module Check exposing (..)


type Val
    = Empty
    | EBool Bool
    | EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    Empty,
    EBool True,
    EInt 1
    ]
