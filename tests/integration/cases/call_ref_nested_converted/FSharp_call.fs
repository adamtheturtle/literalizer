module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_data: obj) : obj = null
let myVar: Val = FInt 42L
process(FList [FMap [("ref", FStr "myVar")]; FInt 42L; FStr "static"])
