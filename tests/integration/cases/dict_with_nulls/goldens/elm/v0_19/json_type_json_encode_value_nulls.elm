module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("name", Json.Encode.string "Alice"),
    ("score", Json.Encode.null),
    ("age", Json.Encode.int 30)
    ]
