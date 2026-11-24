module Check exposing (..)


import Json.Encode


shared : Json.Encode.Value
shared = Json.Encode.string "value"
my_data : Json.Encode.Value
my_data = shared
