module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("drop", ENull),
    ("keep", EInt 1)
    ]
