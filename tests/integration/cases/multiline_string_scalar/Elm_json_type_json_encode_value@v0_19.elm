module Check exposing (..)


import Json.Encode


my_data : Json.Encode.Value
my_data = Json.Encode.string "\nroot first line\n  indented\n\nroot last line\n"
