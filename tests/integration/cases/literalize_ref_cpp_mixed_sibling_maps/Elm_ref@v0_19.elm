module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


actual : Val
actual = EInt 42
my_data : Val
my_data = EList [
    EDict [("$ref", EInt 1)],
    EDict [("$ref", ENull)],
    actual
    ]
