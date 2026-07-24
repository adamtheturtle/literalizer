module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let process (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(process("hello"), "one")
emit(process(42), "zero")
