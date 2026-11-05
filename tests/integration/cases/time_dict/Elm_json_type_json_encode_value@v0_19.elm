module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("morning", Json.Encode.string "09:30:00"),
    ("afternoon", Json.Encode.string "14:15:00"),
    ("evening", Json.Encode.string "23:59:59")
    ]
