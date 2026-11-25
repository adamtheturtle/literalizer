module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("lower", FInt 3735928559L);
    ("upper", FInt 31L);
    ("negative", FInt(-16L));
    ("zero", FInt 0L)
]
