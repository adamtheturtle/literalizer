module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EList [EList [EInt 1, EInt 2], EList [EInt 3]]),
    ("b", EList [EList [], EList [EInt 1]])
    ]
