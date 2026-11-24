module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("ts", EStr "3000-12-31T23:59:59.999999+00:00")
    ]
