module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("within_i32", EStr "2024-01-15T12:00:00"),
    ("beyond_i32", EStr "2099-06-15T08:30:00")
    ]
