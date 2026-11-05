module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("exact_millisecond", EStr "09:30:15.123000"),
    ("sub_millisecond", EStr "09:30:15.123456")
    ]
