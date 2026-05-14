module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("metrics", EDict [("count", EInt 100), ("rate", EInt 50)]),
    ("flags", EDict [("retries", EInt 3), ("timeout", EInt 30)])
    ]
