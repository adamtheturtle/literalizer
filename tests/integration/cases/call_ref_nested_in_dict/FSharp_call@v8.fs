module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_data: obj) : obj = null
let my_var: Val = FInt 42L
process(FMap [("key", my_var); ("count", FInt 42L); ("label", FStr "example")])
