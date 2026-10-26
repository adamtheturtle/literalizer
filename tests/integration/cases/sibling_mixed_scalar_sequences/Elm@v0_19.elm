module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("left", EList [EInt 1, EStr "one"]),
    ("right", EList [EInt 2, EStr "two"])
    ]
