module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "]",
    Json.Encode.string "a]",
    Json.Encode.string "a]=",
    Json.Encode.string "a]b"
    ]
