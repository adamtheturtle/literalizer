module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("scores", EList [EInt 1, EInt 2])],
    EDict [("scores", EList [EInt 3, EInt 4])]
    ]
