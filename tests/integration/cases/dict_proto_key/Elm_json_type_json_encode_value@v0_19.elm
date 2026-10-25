module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.object [
    ("__proto__", Json.Encode.object [("x", Json.Encode.int 1)]),
    ("n", Json.Encode.object [("__proto__", Json.Encode.int 3)]),
    ("y", Json.Encode.int 2)
    ]
