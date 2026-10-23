module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("cr", Json.Encode.string "a\rb"),
    ("crlf", Json.Encode.string "a\r\nb"),
    ("lf", Json.Encode.string "a\nb")
    ]
