module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let foo: Val = FMap [
    ("_", FStr "_")
]
let my_data: Val = FMap [
    ("items", FList [FMap [("other", FInt 1L)]; foo]);
    ("mapping", FMap [("value", foo)])
]
