module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("quote\"backslash\\", EInt 1),
    ("line\nbreak", EInt 2),
    ("$(literal)${text}", EInt 3),
    ("RStr prefix", EInt 4)
    ]
