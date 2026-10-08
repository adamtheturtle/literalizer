module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("_", EList [EInt 1, EFloat 2.5, EInt 3])
    ]
