module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("outer", EList (EList (EStr "nested first line\n  indented\n\nnested last line\n" :: []) :: []))
    ]
