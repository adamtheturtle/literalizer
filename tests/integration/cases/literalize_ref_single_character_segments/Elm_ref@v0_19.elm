module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


aBC : Val
aBC = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = aBC
