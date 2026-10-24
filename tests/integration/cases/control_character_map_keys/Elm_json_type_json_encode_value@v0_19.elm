module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("", Json.Encode.int 1),
    ("a\u{0001}b", Json.Encode.int 2)
    ]
