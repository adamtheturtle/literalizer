module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_value: obj) : obj = null
let existing: Val = FInt 42L
process(existing)
