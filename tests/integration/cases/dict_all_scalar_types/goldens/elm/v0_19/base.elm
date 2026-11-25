module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("s", EStr "string"),
    ("i", EInt 1),
    ("f", EFloat 1.5),
    ("b", EBool True),
    ("n", ENull),
    ("d", EStr "2024-01-15"),
    ("dt", EStr "2024-01-15T12:00:00"),
    ("by", EStr "48656c6c6f")
    ]
