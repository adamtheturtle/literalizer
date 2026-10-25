module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.object [("mapping", Json.Encode.object [])],
    Json.Encode.object []
    ]
