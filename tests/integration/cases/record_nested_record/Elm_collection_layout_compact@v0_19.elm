module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("id", EInt 1),
    ("owner", EDict [("name", EStr "Alice"), ("age", EInt 30)])
    ]
