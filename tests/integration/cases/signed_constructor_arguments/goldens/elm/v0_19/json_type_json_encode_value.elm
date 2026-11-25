module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.int (-42),
    Json.Encode.int 0,
    Json.Encode.int 42,
    Json.Encode.float (-1.25),
    Json.Encode.float 0.0,
    Json.Encode.float 1.25
    ]
