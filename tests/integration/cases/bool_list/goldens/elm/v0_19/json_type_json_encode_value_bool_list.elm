module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.bool True,
    Json.Encode.bool False,
    Json.Encode.bool True
    ]
