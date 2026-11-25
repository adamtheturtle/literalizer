module Check exposing (..)


type Val
    = JInt Int
    | JStr String
    | JDict (List ( String, Val ))


my_data : Val
my_data = JDict [
    ("quote\"backslash\\", JInt 1),
    ("line\nbreak", JInt 2),
    ("$(literal)${text}", JInt 3),
    ("RStr prefix", JInt 4)
    ]
