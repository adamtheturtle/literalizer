module Main

let process (_value: obj) : obj = null
type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
process(FStr "hello")
process(FInt 42L)
process(FBool true)
process(FNull)
