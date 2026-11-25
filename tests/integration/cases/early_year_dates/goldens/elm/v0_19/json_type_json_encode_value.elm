module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("date", Json.Encode.string "0099-05-27"),
    ("naive", Json.Encode.string "0001-01-01T12:30:00"),
    ("recent", Json.Encode.string "2024-05-27T10:00:00")
    ]
