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
    EFloat (-1.250000),
    EFloat 0.000000,
    EFloat 1.250000
    ]
