module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- before	line
    ("value", EStr "left\tright")  -- inline	line
    -- after	line
    ]
