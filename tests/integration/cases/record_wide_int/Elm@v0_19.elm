module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("quantity", EInt 1000000),
    ("big", EInt 18446744073709551615),
    ("ratio", EFloat 2.5),
    ("label", EStr "tag"),
    ("ok", EBool True)
    ]
