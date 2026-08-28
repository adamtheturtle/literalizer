module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("a", Json.Encode.int 1),  -- About a.
    ("b", Json.Encode.int 2)
    ]
