module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_data: obj) : obj = null
let my_var: Val = FInt 42L
let my_other: Val = FInt 7L
process(FList [FMap [("ref", FStr "my_var")]; FInt 42L; FStr "static"])
process(FList [FMap [("ref", FStr "my_other")]; FInt 7L; FStr "label"])
