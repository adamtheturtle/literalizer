module Check exposing (..)


type Val
    = EInt Int
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EInt (-2147483649),
    EInt (-2147483648),
    EInt 2147483647,
    EInt 2147483648
    ]
