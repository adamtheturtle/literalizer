module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_value: obj, _label: obj) : obj = null
process("hello", "a")
process(42, "b")
process(FBool true, "c")
