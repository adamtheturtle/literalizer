module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("quote\"backslash\\", FInt 1L);
    ("line\nbreak", FInt 2L);
    ("$(literal)${text}", FInt 3L);
    ("RStr prefix", FInt 4L)
]
