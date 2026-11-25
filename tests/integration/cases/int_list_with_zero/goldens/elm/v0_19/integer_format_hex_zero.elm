module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 0x0,
    EInt 0x1,
    EInt (-0x1)
    ]
