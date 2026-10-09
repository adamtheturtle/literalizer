module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("v", EStr "a‪\u{0000}é😀b")
    ]
