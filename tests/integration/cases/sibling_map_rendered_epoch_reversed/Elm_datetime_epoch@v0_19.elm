module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("b", EDict [("k", EInt 1)]),
    ("a", EDict [("k", EInt 2208988800)])
    ]
