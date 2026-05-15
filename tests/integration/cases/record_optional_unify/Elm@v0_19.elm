module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("items", EList [EDict [("id", EInt 1)], EDict [("id", EInt 2), ("count", EInt 10)], EDict [("id", EInt 3), ("count", EInt 20)]])
    ]
