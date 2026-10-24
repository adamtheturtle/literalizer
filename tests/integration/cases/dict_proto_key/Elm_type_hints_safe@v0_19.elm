module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("__proto__", EDict [("x", EInt 1)]),
    ("n", EDict [("__proto__", EInt 3)]),
    ("y", EInt 2)
    ]
