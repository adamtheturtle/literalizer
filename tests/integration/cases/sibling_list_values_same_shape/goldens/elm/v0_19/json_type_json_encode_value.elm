module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("test", Json.Encode.list identity [Json.Encode.int 5, Json.Encode.list identity [Json.Encode.string "compile", Json.Encode.string "test"]]),
    ("package", Json.Encode.list identity [Json.Encode.int 7, Json.Encode.list identity [Json.Encode.string "link", Json.Encode.string "test"]])
    ]
