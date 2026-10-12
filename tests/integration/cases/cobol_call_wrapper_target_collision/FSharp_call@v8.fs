module Main

let check (_a: obj) : obj = null
type Val =
    | FInt of int64
check(FInt 42L)
