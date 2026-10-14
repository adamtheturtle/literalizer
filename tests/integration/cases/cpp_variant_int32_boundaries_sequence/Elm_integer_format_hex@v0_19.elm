module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt (-0x80000000),
    EInt (-0x7fffffff),
    EList [EInt 0x0]
    ]
