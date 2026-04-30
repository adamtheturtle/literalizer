module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [EList [EDict [("$ref", EStr "my_var")], EInt 42, EStr "static"]],
    EList [EList [EDict [("$ref", EStr "my_other")], EInt 7, EStr "label"]]
    ]
