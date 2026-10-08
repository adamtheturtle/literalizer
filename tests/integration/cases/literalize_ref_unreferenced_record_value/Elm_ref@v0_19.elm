module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("main", EDict [("x", EInt 1), ("y", EStr "s")])
    ]
