module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("b", ENull),
    ("a", EDict [("y", EList (EFloat 1.0 :: [])), ("x", EBool False)])
    ]
