module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.int 9223372036854775808
