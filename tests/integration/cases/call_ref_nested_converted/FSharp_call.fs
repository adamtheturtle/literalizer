module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_data: obj) : obj = null
let myVar: Val = FInt 42L
process(FList [myVar; FInt 42L; FStr "static"])
