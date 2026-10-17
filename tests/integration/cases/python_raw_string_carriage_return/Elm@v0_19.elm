module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("cr", EStr "a\rb"),
    ("crlf", EStr "a\r\nb"),
    ("lf", EStr "a\nb")
    ]
