module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("quote\"backslash\\", Json.Encode.int 1),
    ("line\nbreak", Json.Encode.int 2),
    ("$(literal)${text}", Json.Encode.int 3),
    ("RStr prefix", Json.Encode.int 4)
    ]
