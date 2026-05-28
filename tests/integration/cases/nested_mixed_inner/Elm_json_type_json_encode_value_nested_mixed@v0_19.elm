module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.list identity [Json.Encode.int 1, Json.Encode.string "a"],
    Json.Encode.list identity [Json.Encode.int 2, Json.Encode.string "b"]
    ]
