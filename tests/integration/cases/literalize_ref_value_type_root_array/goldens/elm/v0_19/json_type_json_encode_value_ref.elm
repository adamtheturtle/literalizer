module Check exposing (..)


import Json.Encode


shared : Json.Encode.Value
shared = Json.Encode.list identity [
    Json.Encode.int 1,
    Json.Encode.int 2
    ]
my_data : Json.Encode.Value
my_data = shared
