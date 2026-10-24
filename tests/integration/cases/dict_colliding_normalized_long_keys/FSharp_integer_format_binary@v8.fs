module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a_b", FInt 0b1L);
    ("a-b", FInt 0b10L);
    ("averyveryverylongkeynamethatgoesonandonandon", FInt 0b11L);
    ("averyveryverylongkeynamethatgoesonandmore", FInt 0b100L)
]
