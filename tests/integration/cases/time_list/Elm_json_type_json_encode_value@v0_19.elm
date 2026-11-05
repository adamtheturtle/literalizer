module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("times", Json.Encode.list identity [Json.Encode.string "09:30:00", Json.Encode.string "17:45:00", Json.Encode.string "23:59:59"])
    ]
