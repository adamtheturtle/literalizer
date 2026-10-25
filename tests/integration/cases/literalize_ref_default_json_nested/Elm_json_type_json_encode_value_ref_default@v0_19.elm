module Check exposing (..)


import Json.Encode


shared : Json.Encode.Value
shared = Json.Encode.int 42
my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("refs", Json.Encode.list identity [shared, shared]),
    ("quoted", Json.Encode.string "#{shared}")
    ]
