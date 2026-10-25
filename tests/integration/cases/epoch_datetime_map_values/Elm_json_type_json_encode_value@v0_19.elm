module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("within_i32", Json.Encode.string "2024-01-15T12:00:00"),
    ("beyond_i32", Json.Encode.string "2099-06-15T08:30:00")
    ]
