module Check exposing (..)


import Json.Encode


arena : Json.Encode.Value
arena = Json.Encode.object [
    ("a", Json.Encode.int 1)
    ]
