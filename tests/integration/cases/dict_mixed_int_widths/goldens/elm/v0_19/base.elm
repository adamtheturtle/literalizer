module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EInt 1),
    ("b", EInt 3000000000),
    ("c", EStr "x")
    ]
