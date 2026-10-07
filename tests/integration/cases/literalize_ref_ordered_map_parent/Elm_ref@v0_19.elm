module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


bound : Val
bound = EInt 2
my_data : Val
my_data = EDict [
    ("value", bound)
    ]
