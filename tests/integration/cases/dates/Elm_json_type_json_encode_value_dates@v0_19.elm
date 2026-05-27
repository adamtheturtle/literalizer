module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("date", Json.Encode.string "2024-01-15"),
    ("datetime", Json.Encode.string "2024-01-15T12:30:00+00:00")
    ]
