module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("exact_millisecond", Json.Encode.string "09:30:15.123000"),
    ("sub_millisecond", Json.Encode.string "09:30:15.123456")
    ]
