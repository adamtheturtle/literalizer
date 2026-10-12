module Main

let process (_IF: obj) : obj = null
type Val =
    | FInt of int64
process(FInt 42L)
