module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


existing : Val
existing = EInt 1
my_data : Val
my_data = EList [
    EInt 0,
    EList [EList [existing]]
    ]
