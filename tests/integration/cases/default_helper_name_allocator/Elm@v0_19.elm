module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


allocator : Val
allocator = EDict [
    ("a", EInt 1)
    ]
