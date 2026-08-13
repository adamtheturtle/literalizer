module Check exposing (..)


type Val
    = EFloat Float
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("value", EFloat 1.2345678901234567)
    ]
