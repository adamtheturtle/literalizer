module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("cr", FStr "a\rb");
    ("crlf", FStr "a\r\nb");
    ("lf", FStr "a\nb")
]
