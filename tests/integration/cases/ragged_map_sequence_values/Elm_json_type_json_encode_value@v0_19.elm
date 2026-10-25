module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("a", Json.Encode.list identity [Json.Encode.object [("item", Json.Encode.list identity [Json.Encode.int 1])]]),
    ("b", Json.Encode.list identity [Json.Encode.object [("item", Json.Encode.list identity [Json.Encode.int 2, Json.Encode.int 3])]])
    ]
