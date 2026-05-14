module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let process (_value: obj) : obj = null
process(FMap [("a", FInt 1L); ("b", FStr "x")])
