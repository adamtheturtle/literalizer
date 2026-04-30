module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("$ref", EStr "my_var")
    ]
