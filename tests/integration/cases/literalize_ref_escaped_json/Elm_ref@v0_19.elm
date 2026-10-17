module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


existing : Val
existing = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = existing
