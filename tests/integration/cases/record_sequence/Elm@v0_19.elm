module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("id", EInt 1), ("label", EStr "first")],
    EDict [("id", EInt 2), ("label", EStr "second")],
    EDict [("id", EInt 3), ("label", EStr "third")]
    ]
