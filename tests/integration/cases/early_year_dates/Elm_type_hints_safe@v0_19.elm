module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("date", EStr "0099-05-27"),
    ("naive", EStr "0001-01-01T12:30:00"),
    ("recent", EStr "2024-05-27T10:00:00")
    ]
