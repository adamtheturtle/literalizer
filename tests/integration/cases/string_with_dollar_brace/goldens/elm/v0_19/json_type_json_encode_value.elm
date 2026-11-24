module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "prefix ${HOME} suffix",
    Json.Encode.string "${interpolated}"
    ]
