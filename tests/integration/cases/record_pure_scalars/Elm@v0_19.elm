module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("name", EStr "Alice"),
    ("age", EInt 30),
    ("active", EBool True),
    ("score", EFloat 4.5)
    ]
