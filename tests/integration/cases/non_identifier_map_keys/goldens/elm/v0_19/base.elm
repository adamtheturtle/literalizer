module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a-b", EInt 1),
    ("two words", EInt 2),
    ("she said \"hi\"", EInt 3),
    ("", EInt 4),
    ("valid_key", EInt 5)
    ]
