module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("a", EInt 1)],
    EInt 1,
    EStr "x",
    EBool True,
    EFloat 2.5,
    ENull
    ]
