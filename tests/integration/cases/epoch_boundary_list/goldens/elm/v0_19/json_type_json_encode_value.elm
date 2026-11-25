module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "1901-12-13T20:45:51",
    Json.Encode.string "1901-12-13T20:45:52",
    Json.Encode.string "2038-01-19T03:14:07",
    Json.Encode.string "2038-01-19T03:14:08"
    ]
