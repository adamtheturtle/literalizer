module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.int (-2147483649)
