module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


k : Val
k = EDict [
    ("a", EInt 1)
    ]
