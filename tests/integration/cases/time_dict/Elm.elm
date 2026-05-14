module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("morning", "09:30:00"),
    ("afternoon", "14:15:00"),
    ("evening", "23:59:59")
    ]
