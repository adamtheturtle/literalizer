module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EInt 1),
    ("b", EStr "x"),
    ("e", EList [EInt 1, EInt 2]),
    ("f", EDict [("g", EStr "h")])
    ]
