module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("v", Json.Encode.string "a‪\u{0000}é😀b")
    ]
