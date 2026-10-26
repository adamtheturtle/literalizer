module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.float 5.0e-324,
    Json.Encode.float (-5.0e-324),
    Json.Encode.float 1.0e-310
    ]
