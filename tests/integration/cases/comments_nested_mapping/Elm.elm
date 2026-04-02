module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EDict [("x", EInt 1)]),
    ("b", EInt 2)
    ]
