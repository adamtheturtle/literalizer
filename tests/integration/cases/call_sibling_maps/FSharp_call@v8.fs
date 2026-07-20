module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_value: obj) : obj = null
process(FMap [("value", FInt 1L)])
process(FMap [("value", FStr "hello")])
