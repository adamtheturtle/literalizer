module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a_b", FInt 0x1L);
    ("a-b", FInt 0x2L);
    ("averyveryverylongkeynamethatgoesonandonandon", FInt 0x3L);
    ("averyveryverylongkeynamethatgoesonandmore", FInt 0x4L)
]
