module Main

let check_wrapper (_a: obj) : obj = null
type Val =
    | FInt of int64
check_wrapper(FInt 42L)
