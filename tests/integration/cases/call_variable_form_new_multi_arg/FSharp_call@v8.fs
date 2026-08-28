module Main

let record_entry (_s: obj, _n: obj, _b: obj) : obj = null
type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data = record_entry(FStr "a", FInt 1L, FBool true)
