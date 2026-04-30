module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [EDict [("key", EDict [("$ref", EStr "my_var")]), ("count", EInt 42)]]
    ]
