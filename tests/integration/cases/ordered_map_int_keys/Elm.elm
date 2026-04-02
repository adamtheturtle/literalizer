module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("1", EStr "one"),
    ("2", EStr "two"),
    ("42", EStr "answer")
    ]
