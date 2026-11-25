module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


std : Val
std = EDict [
    ("a", EInt 1)
    ]
