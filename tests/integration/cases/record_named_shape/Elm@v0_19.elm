module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("id", EInt 100), ("label", EStr "first item"), ("enabled", EBool False), ("related_ids", EList [EInt 102, EInt 103])],
    EDict [("id", EInt 101), ("label", EStr "second item"), ("enabled", EBool True), ("related_ids", EList [EInt 100])]
    ]
