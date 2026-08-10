module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("x", EStr "\u{0000}"),
    ("y", EStr "\u{0000}1")
    ]
