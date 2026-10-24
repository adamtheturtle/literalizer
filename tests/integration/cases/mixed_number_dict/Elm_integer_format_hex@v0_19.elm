module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EInt 0x1),
    ("b", EFloat 2.5),
    ("c", EInt 0x3)
    ]
