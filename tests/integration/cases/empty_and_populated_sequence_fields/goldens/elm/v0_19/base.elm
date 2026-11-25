module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("value", EList [])],
    EDict [("value", EList (EInt 1 :: []))]
    ]
