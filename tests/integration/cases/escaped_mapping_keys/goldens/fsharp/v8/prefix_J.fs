module Main

type Val =
    | JInt of int64
    | JStr of string
    | JMap of (string * Val) list
let my_data: Val = JMap [
    ("quote\"backslash\\", JInt 1L);
    ("line\nbreak", JInt 2L);
    ("$(literal)${text}", JInt 3L);
    ("RStr prefix", JInt 4L)
]
