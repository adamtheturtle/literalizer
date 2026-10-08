module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("groups", [|[|FMap [("id", FInt 1L)]|]; [|FMap [("id", FInt 2L)]|]|])
]
