module Check exposing (..)


import Json.Encode


my_data = Json.Encode.object [
    ("name", Json.Encode.string "Alice"),
    ("scores", Json.Encode.list identity [Json.Encode.int 10, Json.Encode.int 20, Json.Encode.int 30])
    ]
