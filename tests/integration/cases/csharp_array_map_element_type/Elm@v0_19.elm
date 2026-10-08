module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("d", EList [EDict [("a", EList [EDict [("b", EList [EInt 1, EList [EFloat 2.5, EList [EStr "x", EList [EBool True]]]])]])]])
    ]
