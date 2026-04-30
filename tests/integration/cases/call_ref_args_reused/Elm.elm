module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [EDict [("$ref", EStr "repeated_var")], EInt 1],
    EList [EDict [("$ref", EStr "single_var")], EInt 0],
    EList [EDict [("$ref", EStr "repeated_var")], EInt 8]
    ]
