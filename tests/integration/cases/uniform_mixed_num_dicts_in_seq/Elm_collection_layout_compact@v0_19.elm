module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("x", EInt 1), ("y", EFloat 2.5)],
    EDict [("x", EInt 3), ("y", EFloat 4.0)]
    ]
