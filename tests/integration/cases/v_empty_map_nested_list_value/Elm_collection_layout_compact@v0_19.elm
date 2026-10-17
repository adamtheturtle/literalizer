module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [EDict [("values", EList (EList [] :: []))], EDict []],
    EList [EDict [], EDict [("values", EList (EList [] :: []))]]
    ]
