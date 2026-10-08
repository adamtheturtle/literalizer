module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("_", EDict [("a", EInt 1), ("b", EInt 2)])
    ]
