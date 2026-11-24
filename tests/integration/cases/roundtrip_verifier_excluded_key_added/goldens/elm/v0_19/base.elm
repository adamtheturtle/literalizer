module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("keep", EBool True),
    ("skip", EInt 0)
    ]
