module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("morning", EStr "09:30:00"),
    ("afternoon", EStr "14:15:00"),
    ("evening", EStr "23:59:59")
    ]
