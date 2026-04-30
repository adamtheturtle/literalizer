module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


x : Val
x = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EList [
    x,
    EInt 1,
    EInt 2
    ]
