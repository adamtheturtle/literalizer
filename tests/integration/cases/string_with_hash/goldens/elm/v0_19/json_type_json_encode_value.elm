module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "issue #{42}",
    Json.Encode.string "color #red"
    ]
