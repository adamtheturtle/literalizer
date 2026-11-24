module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    (* {- and {- stay readable *)
    (* balanced {- nested -} and trailing -} stay readable *)
    ("x", FInt 1L)
]
