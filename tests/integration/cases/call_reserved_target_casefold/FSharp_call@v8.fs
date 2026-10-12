module Main

let BEGIN (_a: obj) : obj = null
type Val =
    | FInt of int64
BEGIN(FInt 42L)
