module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("__proto__", Json.Encode.object [("x", Json.Encode.int 1)]),
    ("ordinary", Json.Encode.int 2)
    ]
