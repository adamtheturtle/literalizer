module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("name", EStr "Alice"),
    ("age", EInt 30),
    ("active", EBool True),
    ("score", ENull),
    ("joined", EStr "2024-01-15"),
    ("last_login", EStr "2024-01-15T12:30:00+00:00"),
    ("avatar", EStr "48656c6c6f")
    ]
