module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("name", EStr "Alice"), ("age", EInt 30)],
    EDict [("name", EStr "Bob"), ("age", EInt 25)]
    ]
