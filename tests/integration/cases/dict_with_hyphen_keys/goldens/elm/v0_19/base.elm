module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("my-key", EStr "value1"),
    ("another-key", EStr "value2"),
    ("normal_key", EStr "value3")
    ]
