module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    Json.Encode.int 1
    ]
