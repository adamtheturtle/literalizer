module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EList [EList [EInt 1, EInt 2]]),
    ("b", EList [EList [EInt 3]])
    ]
