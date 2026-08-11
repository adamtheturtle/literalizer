module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a_b", FInt 1L);
    ("a-b", FInt 2L);
    ("averyveryverylongkeynamethatgoesonandonandon", FInt 3L);
    ("averyveryverylongkeynamethatgoesonandmore", FInt 4L)
]
