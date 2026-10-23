module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a_b", FInt 0o1L);
    ("a-b", FInt 0o2L);
    ("averyveryverylongkeynamethatgoesonandonandon", FInt 0o3L);
    ("averyveryverylongkeynamethatgoesonandmore", FInt 0o4L)
]
