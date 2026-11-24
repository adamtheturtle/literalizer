module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("first", EDict [("x", EInt 1)]),
    ("second", EDict [("y", EInt 2)])
    ]
