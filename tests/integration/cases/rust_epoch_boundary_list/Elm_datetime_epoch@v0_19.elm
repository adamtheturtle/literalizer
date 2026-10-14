module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt (-2147483649),
    EInt (-2147483648),
    EInt 2147483647,
    EInt 2147483648
    ]
