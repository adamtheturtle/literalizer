module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EInt 1, EStr "two"],
    EList []
    ]
