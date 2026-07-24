module Main

type Val =
    | FInt of int64
    | FList of Val list
let process (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(process(42), 1)
