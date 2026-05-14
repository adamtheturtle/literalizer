module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("date", EStr "2024-01-15"),
    ("datetime", EStr "2024-01-15T12:30:00+00:00")
    ]
