module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("", EInt 1),
    ("a\u{0001}b", EInt 2)
    ]
