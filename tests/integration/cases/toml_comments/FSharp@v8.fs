module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // before
    ("answer", FInt 42L);  // inline
    ("plain", FStr "ok")
    // trailing
]
