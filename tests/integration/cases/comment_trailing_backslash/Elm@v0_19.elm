module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- comment ending backslash \ .
    ("x", EInt 1)
    ]
