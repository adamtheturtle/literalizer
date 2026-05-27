module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("name", Json.Encode.string "Alice"),
    ("age", Json.Encode.int 30),
    ("active", Json.Encode.bool True)
    ]
