module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


arena : Val
arena = EDict [
    ("a", EInt 1)
    ]
