module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


siblingMap : Val
siblingMap = EDict [
    ("k", EInt 2)
    ]
my_data : Val
my_data = EList [
    EDict [("k", EInt 1)],
    siblingMap
    ]
