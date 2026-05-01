module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let send (_value: obj) : obj = null
send(FMap [("a", FInt 1L); ("b", FStr "x")])
