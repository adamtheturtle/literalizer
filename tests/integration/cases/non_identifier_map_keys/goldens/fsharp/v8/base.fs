module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a-b", FInt 1L);
    ("two words", FInt 2L);
    ("she said \"hi\"", FInt 3L);
    ("", FInt 4L);
    ("valid_key", FInt 5L)
]
