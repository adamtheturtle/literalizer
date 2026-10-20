module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


key_binding : Val
key_binding = EDict [
    ("a", EInt 1)
    ]
