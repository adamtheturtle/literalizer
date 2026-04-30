module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


refX : Val
refX = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EList [
    refX,
    EInt 1,
    EInt 2
    ]
