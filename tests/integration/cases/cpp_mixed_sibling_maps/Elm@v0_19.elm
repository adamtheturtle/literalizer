module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [EDict [("a", EInt 1)], EDict [("a", ENull)], EInt 42],
    EList [EDict [("a", EInt 1)], EDict [("a", EStr "s")], EInt 42],
    EList [EDict [("a", EInt 1)], EDict [("a", ENull)]],
    EList [EDict [("a", EInt 1)], EDict [("a", EStr "s")]]
    ]
