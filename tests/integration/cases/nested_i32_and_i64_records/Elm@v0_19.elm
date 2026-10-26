module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList (EDict [("value", EInt 1)] :: []),
    EList (EDict [("value", EInt 1099511627776)] :: [])
    ]
