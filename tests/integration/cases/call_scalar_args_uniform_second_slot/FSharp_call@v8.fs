module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_value: obj, _label: obj) : obj = null
process(FStr "hello", FStr "a")
process(FInt 42L, FStr "b")
process(FBool true, FStr "c")
