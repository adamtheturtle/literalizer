module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("__proto__", EDict [("x", EInt 1)]),
    ("ordinary", EInt 2)
    ]
