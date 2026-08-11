module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 999999999999999999,
    EInt (-999999999999999999)
    ]
