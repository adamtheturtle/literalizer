module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "line1\r\nline2",
    Json.Encode.string "line1\rline2",
    Json.Encode.string "\u{0001}"
    ]
