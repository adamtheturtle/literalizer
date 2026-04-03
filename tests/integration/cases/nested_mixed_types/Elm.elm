module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EInt 1, EInt 2],
    EList [EStr "a", EStr "b"]
    ]
