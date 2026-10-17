module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


value : Val
value = EStr "12:30:15+02:00"
my_data : Val
my_data = EDict [
    ("x", value)
    ]
