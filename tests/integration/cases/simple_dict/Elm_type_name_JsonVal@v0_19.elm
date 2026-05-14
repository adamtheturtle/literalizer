module Check exposing (..)


type JsonVal
    = ENull
    | EBool Bool
    | EInt Int
    | EStr String
    | EDict (List ( String, JsonVal ))


my_data : JsonVal
my_data = EDict [
    ("name", EStr "Alice"),
    ("age", EInt 30),
    ("active", EBool True),
    ("score", ENull)
    ]
