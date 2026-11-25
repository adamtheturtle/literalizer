module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "2024-01-15",
    Json.Encode.string "2024-06-01"
    ]
