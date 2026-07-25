module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("first", EStr "Alice"), ("last", EStr "Smith")],
    EDict [("first", EStr "Bob"), ("middle", EStr "Quincy")]
    ]
