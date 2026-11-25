module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.list identity [Json.Encode.string "\nfirst line\n  indented\n\nlast line\n"]
    ]
