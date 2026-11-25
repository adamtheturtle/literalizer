module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("name", EStr "Alice"),
    ("scores", EList [EInt 10, EInt 20, EInt 30])
    ]
