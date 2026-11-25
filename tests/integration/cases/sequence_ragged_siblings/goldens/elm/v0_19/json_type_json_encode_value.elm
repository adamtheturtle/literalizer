module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.list identity [Json.Encode.string "set_task", Json.Encode.string "web", Json.Encode.string "lint_web"],
    Json.Encode.list identity [Json.Encode.string "merge_pipelines"]
    ]
