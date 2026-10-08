module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("double", EStr "a b"),
    ("single", EStr "c d"),
    ("both", EStr "e f g"),
    ("continued", EStr "hi"),
    ("escaped backslash", EStr "j\\ k")
    ]
