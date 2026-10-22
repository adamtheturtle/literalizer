module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "café",
    Json.Encode.string "中文",
    Json.Encode.string "😀"
    ]
