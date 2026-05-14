module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 1000000,
    EInt (-1234),
    EInt 255,
    EInt (-10)
    ]
