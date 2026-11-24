module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EFloat 2.500000,
    EInt 1
    ]
