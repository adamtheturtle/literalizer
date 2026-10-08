module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("a", EList [EInt 1])],
    EDict [("a", EList [EInt 2])]
    ]
