module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 1,
    EInt 1099511627776
    ]
