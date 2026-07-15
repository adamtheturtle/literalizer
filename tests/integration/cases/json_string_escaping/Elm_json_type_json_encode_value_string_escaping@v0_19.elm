module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.string "a\"b\tcé"
