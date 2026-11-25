module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "C:\\path\\to\\file",
    Json.Encode.string "back\\\\slash",
    Json.Encode.string "hello \\\"world\\\"",
    Json.Encode.string "path\\to \"# file",
    Json.Encode.string "trailing\\",
    Json.Encode.string "both \"quotes''' here",
    Json.Encode.string "line1\\nline2\nwith newline"
    ]
