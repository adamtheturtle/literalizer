module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("$ref", EStr "ref_x")],
    EInt 1,
    EInt 2
    ]
