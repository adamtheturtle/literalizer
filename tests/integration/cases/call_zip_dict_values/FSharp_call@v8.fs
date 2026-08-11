module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(process(FStr "hello"), FMap [("a", FInt 1L); ("b", FInt 2L)])
emit(process(FInt 42L), FMap [("c", FInt 3L); ("d", FInt 4L)])
