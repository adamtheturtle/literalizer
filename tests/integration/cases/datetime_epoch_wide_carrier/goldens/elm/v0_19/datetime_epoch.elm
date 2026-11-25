module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("within_i32", EInt 1705320000),
    ("beyond_i32", EInt 4085195400)
    ]
