module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


shared : Val
shared = EStr "a\u{0000}b"
my_data : Val
my_data = EDict [
    ("value", shared)
    ]
