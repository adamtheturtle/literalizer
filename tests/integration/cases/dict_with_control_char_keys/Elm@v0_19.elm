module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("key\nwith\nnewlines", EStr "value1"),
    ("key\twith\ttabs", EStr "value2"),
    ("", EStr "value3")
    ]
