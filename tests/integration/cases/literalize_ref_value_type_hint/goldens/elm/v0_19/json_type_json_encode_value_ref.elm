module Check exposing (..)


import Json.Encode


refData : Json.Encode.Value
refData = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
my_data : Json.Encode.Value
my_data = refData
