module Main

let process (_count: obj) : obj = null
type Val =
    | FInt of int64
process(FInt 42L)
