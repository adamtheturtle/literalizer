module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt (-42),
    EInt 0,
    EInt 42,
    EFloat (-1.25),
    EFloat 0.0,
    EFloat 1.25
    ]
