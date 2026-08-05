module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.int 9223372036854775807,
    Json.Encode.int 9223372036854775808
    ]
