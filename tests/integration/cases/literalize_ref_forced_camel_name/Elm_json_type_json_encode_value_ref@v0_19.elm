module Check exposing (..)


import Json.Encode


userObj : Json.Encode.Value
userObj = Json.Encode.object [
    ("_", Json.Encode.string "_")
    ]
my_data : Json.Encode.Value
my_data = userObj
