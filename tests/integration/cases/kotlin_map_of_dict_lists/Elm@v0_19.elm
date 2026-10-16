module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EList [EDict [("k", EInt 1)]]),
    ("b", EList [EDict [("k", EInt 2)]])
    ]
