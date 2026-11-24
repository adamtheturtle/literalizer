module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("first", EDict [("x", EInt 1), ("y", EInt 2)]),
    ("second", EDict [("z", EInt 3)])
    ]
