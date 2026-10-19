module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList (EDict [("a", EInt 1)] :: []),
    EList (EDict [("a", EInt 2)] :: [])
    ]
