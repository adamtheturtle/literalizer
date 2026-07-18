module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 9223372036854775807,
    EInt 9223372036854775808
    ]
