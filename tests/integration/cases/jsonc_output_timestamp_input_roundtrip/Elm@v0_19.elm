module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- event time
    ("when", EStr "2024-01-15T12:34:56+00:00")
    ]
