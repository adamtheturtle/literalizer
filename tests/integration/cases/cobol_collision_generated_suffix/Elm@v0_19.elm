module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a-b", EInt 1),
    ("a b", EInt 2),
    ("a-b-2", EInt 3)
    ]
