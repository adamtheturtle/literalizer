module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("key\nwith\nnewlines", FStr "value1");
    ("key\twith\ttabs", FStr "value2");
    ("", FStr "value3")
]
