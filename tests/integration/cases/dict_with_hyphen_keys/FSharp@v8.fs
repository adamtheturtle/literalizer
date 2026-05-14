module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("my-key", FStr "value1");
    ("another-key", FStr "value2");
    ("normal_key", FStr "value3")
]
