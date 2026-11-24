module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "100% done",
    Json.Encode.string "%(name) is here"
    ]
