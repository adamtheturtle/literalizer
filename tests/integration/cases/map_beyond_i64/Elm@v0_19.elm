module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EInt 9223372036854775807),
    ("b", EInt 9223372036854775808)
    ]
