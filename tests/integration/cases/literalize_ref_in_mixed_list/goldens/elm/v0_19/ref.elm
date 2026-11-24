module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


refX : Val
refX = EInt 3
my_data : Val
my_data = EList [
    refX,
    EInt 1,
    EInt 2
    ]
