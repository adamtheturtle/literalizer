module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FList of Val list
let process (_value: obj) : obj = null
let emit (__call: obj, __zip: obj) : obj = null
emit(process(FInt 42L), FBool true)
