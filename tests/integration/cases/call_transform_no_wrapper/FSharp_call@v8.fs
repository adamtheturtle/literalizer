module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
process(FStr "hello")
process(FInt 42L)
process(FBool true)
