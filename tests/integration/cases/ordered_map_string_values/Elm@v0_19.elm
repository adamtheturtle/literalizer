module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("first", EStr "one"),
    ("second", EStr "two"),
    ("third", EStr "three")
    ]
