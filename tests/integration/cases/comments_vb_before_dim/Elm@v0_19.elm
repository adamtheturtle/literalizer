module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- Configuration
    ("name", EStr "app"),
    -- Port setting
    ("port", EInt 3000)
    ]
