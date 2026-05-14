module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- Server configuration
    ("host", EStr "localhost"),  -- default host
    ("port", EInt 8080),
    -- Enable debug mode
    ("debug", EBool True)
    ]
