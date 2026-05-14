module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("host", EStr "localhost"),
    ("port", ENull),  -- not configured yet
    ("debug", EBool True)
    ]
