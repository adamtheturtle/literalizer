module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("a", Json.Encode.object []),
    ("b", Json.Encode.int 1)
    ]
