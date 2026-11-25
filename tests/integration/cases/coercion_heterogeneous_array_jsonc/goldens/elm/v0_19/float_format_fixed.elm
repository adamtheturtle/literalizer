module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 1,
    EFloat 2.500000,
    EInt 3
    ]
