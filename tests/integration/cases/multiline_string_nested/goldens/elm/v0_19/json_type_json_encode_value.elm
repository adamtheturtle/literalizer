module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("outer", Json.Encode.list identity [Json.Encode.list identity [Json.Encode.string "nested first line\n  indented\n\nnested last line\n"]])
    ]
