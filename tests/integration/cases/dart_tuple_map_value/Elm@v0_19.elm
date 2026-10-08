module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("rows", EList [EDict [("x", EInt 1), ("y", EStr "a")], EDict [("x", EInt 2), ("y", EStr "b")]])
    ]
