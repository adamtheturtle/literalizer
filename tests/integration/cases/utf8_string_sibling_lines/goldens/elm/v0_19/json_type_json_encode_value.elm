module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.list identity [
    Json.Encode.string "中中中中中中中中中中中中中中中中中中中中",
    Json.Encode.string "é'é'é'é'é'é'é'é'é'é'",
    Json.Encode.string "🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂🙂"
    ]
