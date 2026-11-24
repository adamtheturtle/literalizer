module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("starts_at", Json.Encode.string "09:30:00")
    ]
