module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


stringMap : Val
stringMap = EDict [
    ("k", EStr "s")
    ]
my_data : Val
my_data = EList [
    stringMap,
    EDict [("k", EInt 1)]
    ]
