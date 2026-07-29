module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("$key", Json.Encode.string "a\"b\tcé #{world} $ident")
    ]
